from dataclasses import dataclass
import itertools
import re

from lxml import etree

from tocky.ia import extract_page_index, get_djvu_pages, get_page_scan, ocaid_to_djvu_url
from tocky.ocr import ocr_djvu_page
from tocky.utils import avg_ocr_conf

TOC_PAGE_DETECTOR_VERSION = [
    ('v2.E.1', 'Fix: Don\'t check every page after TOC found!'),
    ('v2.E.0', 'Add support for re-ocring when ending TOC range to avoid missing last page(s)'),
    ('v2.D.0', 'Add support for re-ocring previous page once first TOC page detected to avoid missing first page'),
]

@dataclass
class TOCDetectorHyperParams:
  min_lines_with_nums: int = 5
  max_lines_with_nums: int = 50
  max_repeated_nums: int = 4
  min_word_confidence: float = 40
  min_mean_word_confidence: float = 30
  min_small_nums_count_for_first: int = 4
  min_avg_word_len: float = 3.8
  min_increasing_percent: float = 0.75


@dataclass
class TOCAnalysisResult:
  is_toc: bool = False
  failure: str | None = None
  reran_ocr: bool = False
  used_new_ocr: bool = False

def analyze_page_for_toc(
  elem: etree._Element,
  has_begun = False,
  allow_reocr=True,
  redo_ocr=False,
) -> TOCAnalysisResult:
  hiddentext = elem.find(".//HIDDENTEXT")
  if hiddentext is None:
    return TOCAnalysisResult(False, 'Missing hiddentext')

  P = TOCDetectorHyperParams()
  result = TOCAnalysisResult()

  page_file: str = elem.xpath('./@usemap')[0]
  ocaid = page_file.rsplit('_', 1)[0]
  leaf_num = extract_page_index(page_file)
  # print('analyze_page_for_toc', page_file, f'{allow_reocr=}')

  def do_redo_ocr(min_conf: float):
    if elem.xpath('.//HIDDENTEXT/@x-re-ocrd') == ['true']:
      return
    new_ocr = ocr_djvu_page(get_page_scan(ocaid, leaf_num))
    result.reran_ocr = True
    new_ocr_el = etree.fromstring(new_ocr).find('.//HIDDENTEXT')
    # Re-OCR will always output confidences, so assume 100 (likely empty page)
    new_conf = avg_ocr_conf(new_ocr_el) or 100
    # print(f'{page_file} mean_conf {(mean_conf or 0):.2f} -> {new_conf:.2f}')
    if new_conf > min_conf:
      result.used_new_ocr = True
      elem.replace(elem.find('.//HIDDENTEXT'), new_ocr_el)
      return analyze_page_for_toc(elem, has_begun, allow_reocr=False, redo_ocr=False)

  mean_conf = avg_ocr_conf(elem)

  if redo_ocr:
    if new_result := do_redo_ocr(min_conf=(mean_conf or 0) - 15):
      return new_result

  if mean_conf is not None and mean_conf < P.min_mean_word_confidence:
    if allow_reocr:
      if new_result := do_redo_ocr(min_conf=mean_conf):
        return new_result
    return TOCAnalysisResult(False, f'Mean page confidence too low ({mean_conf:.2f} < {P.min_mean_word_confidence})')

  # If there are more than 40 words and the average right coord of each word is
  # less than 2/3 width of page, then potentially should re-ocr cause mis-OCR'd
  # pages
  if allow_reocr:
    word_rights = [
        int(coord.split(',')[2])
        for coord in hiddentext.xpath('.//WORD/@coords')
    ]
    if len(word_rights) > 70:
      width = int(elem.xpath('./@width')[0])
      words_near_right = len([r for r in word_rights if r > width * .8 ])

      words_near_right_text = [
          word.text
          for word in hiddentext.xpath('.//WORD')
          if int(word.xpath('./@coords')[0].split(',')[2]) > width * .8
      ]
      numeric_words_near_right = len([
          word
          for word in words_near_right_text
          if re.search(r'\b([\dxvil]+)$', word) and re.search(r'\d[.,-]\d+$', word) is None
      ])
      # print(f'{words_near_right=}, {numeric_words_near_right=} of {len(word_rights)=}')
      if (words_near_right - numeric_words_near_right) < 3:
        if new_result := do_redo_ocr(min_conf=(mean_conf or 0) - 15):
          return new_result


  numbers_at_end_of_lines = []
  for line in hiddentext.findall(".//LINE"):
      words = line.findall(".//WORD")
      if words:
        last_word = words[-1]
        if (m := re.search(r'\b([\dxvil]+)$', last_word.text)) and re.search(r'\d[.,-]\d+$', last_word.text) is None:
            confidence = last_word.xpath('./@x-confidence')
            bad_ocr = confidence and float(confidence[0]) < P.min_word_confidence
            if len(m.group()) == 1 and bad_ocr:
              # Exclude, likely noise
              pass
            else:
              numbers_at_end_of_lines.append(m.group())

  from collections import Counter
  max_repeated = max(Counter(numbers_at_end_of_lines).values(), default=0)
  lines_w_uniq_nums = len(set(numbers_at_end_of_lines))

  if max_repeated > P.max_repeated_nums:
    return TOCAnalysisResult(False, 'Too many repeated numbers')

  if lines_w_uniq_nums < P.min_lines_with_nums:
    return TOCAnalysisResult(False, f'Not enough lines with nums ({lines_w_uniq_nums} < {P.min_lines_with_nums})')

  if lines_w_uniq_nums > P.max_lines_with_nums:
     return TOCAnalysisResult(False, 'Too many lines with nums')

  nums = [
      int(n.strip())
      for n in numbers_at_end_of_lines
      if n.strip().isnumeric()
  ]
  increasing_count = 0
  non_increasing_count = 0
  for (prev, cur) in itertools.pairwise([0] + nums):
    if prev <= cur:
      increasing_count += 1
    else:
      non_increasing_count += 1

  increasing_percent = increasing_count / (increasing_count + non_increasing_count)
  if len(nums) > 4 and increasing_percent < P.min_increasing_percent:
    return TOCAnalysisResult(False, f'Not enough of the nums are increasing {increasing_percent:.2f} < {P.min_increasing_percent}')

  if has_begun:
    first_line = ' '.join(word.text for word in hiddentext.find(".//LINE").findall(".//WORD"))
    if 'illustration' in first_line.lower() or 'index' in first_line.lower() or 'figure' in first_line.lower() or 'tables' in first_line.lower():
      return TOCAnalysisResult(False, 'Contains illustration/index')
  else:
    small_nums_count = len([n for n in numbers_at_end_of_lines if len(n) < 4])
    if small_nums_count < P.min_small_nums_count_for_first:
      return TOCAnalysisResult(False, 'Not enough small numbers for first TOC page')

    # Check average word length probably bad OCR on empty page
    word_lens = [
        len(word.text.strip())
        for word in elem.findall('.//WORD')
        if not re.search(r'^(\d+|[xvil]+|[\.^;:{}]+)$', word.text.strip(), re.IGNORECASE)
    ]
    avg_word_len = sum(word_lens) / len(word_lens)
    if avg_word_len < P.min_avg_word_len:
      return TOCAnalysisResult(False, f'Average word length too low {avg_word_len:.2f} < {P.min_avg_word_len}')

  if allow_reocr:
    if new_result := do_redo_ocr(min_conf=(mean_conf or 0) - 15):
      return new_result

  return TOCAnalysisResult(True)

def analyze_djvu_for_toc(djvu_url: str, allow_reocr=True):
    has_begun = False
    reocrs_done = 0
    last_result: tuple[str, etree._Element, TOCAnalysisResult] = None
    for page_name, elem in get_djvu_pages(djvu_url, 1, 28):
      toc_analysis = analyze_page_for_toc(elem, has_begun, allow_reocr=allow_reocr and (has_begun or reocrs_done < 10))
      if toc_analysis.reran_ocr:
        reocrs_done += 1
      # Let's check predecessor with redone ocr
      if not has_begun and toc_analysis.is_toc and last_result and not last_result[2].reran_ocr:
        # Check if number is too high before redoing OCR
        recheck_previous = False
        for line in elem.findall(".//LINE"):
            words = line.findall(".//WORD")
            if words:
              last_word = words[-1]
              if bool(re.search(r'\b([xvil]+)$', last_word.text)):
                recheck_previous = False
                break

              if number_m := re.search(r'\b(\d+)$', last_word.text):
                n = int(number_m[1])
                recheck_previous = n > 25
                break

        if recheck_previous:
          new_toc_analysis = analyze_page_for_toc(last_result[1], False, redo_ocr=True)
          reocrs_done += 1
          if new_toc_analysis.is_toc:
            last_result = (last_result[0], last_result[1], new_toc_analysis)

      if has_begun and not toc_analysis.is_toc and not toc_analysis.reran_ocr:
        # Let's try again with rerun ocr
        reocrs_done += 1
        toc_analysis = analyze_page_for_toc(elem, has_begun, redo_ocr=True)

      # Yield the thing we know won't change anymore
      if last_result:
        yield (last_result[0], etree.tostring(last_result[1], encoding='unicode'), last_result[2])

      has_begun = toc_analysis.is_toc
      last_result = (page_name, elem, toc_analysis)

    if last_result:
      yield (last_result[0], etree.tostring(last_result[1], encoding='unicode'), last_result[2])


def detect_table_of_contents_pages(djvu_url: str, allow_reocr=True):
  has_begun = False
  for (page_number, elem_str, toc_analysis) in analyze_djvu_for_toc(djvu_url, allow_reocr=allow_reocr):
    if has_begun and not toc_analysis.is_toc:
      break
    if toc_analysis.is_toc:
      has_begun = True
      yield (page_number, elem_str)



def extract_pages(djvu_url: str, pages: list[int]):
    to_see = set(pages)
    for page_name, elem in get_djvu_pages(djvu_url):
      page_index = extract_page_index(page_name)
      if page_index in to_see:
        yield (page_name, etree.tostring(elem, encoding="unicode"))
        to_see.remove(page_index)
        if not to_see:
          break

def extract_toc_pages(ocaid: str, allow_reocr = True):
  return detect_table_of_contents_pages(ocaid_to_djvu_url(ocaid), allow_reocr=allow_reocr)
