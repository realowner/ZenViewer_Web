import math
import re


class TimeToRead:

    def determine(str_time, div_height):

        num_in_str = ''
        num_without_str = re.findall(r'\d+', str_time)
        if len(num_without_str) > 1:
            num_without_str[-1] = '.' + num_without_str[-1]
            for item in num_without_str:
                num_in_str += item
            total_num = float(num_in_str)
        else:
            total_num = int(num_without_str[0])

        if 'мин.' in str_time:
            thread_num = int(total_num * 60)
        elif 'сек.' in str_time:
            thread_num = total_num

        article_height = div_height + 500.0
        scroll_down = 700.0/2
        scrolls = math.ceil(article_height/scroll_down)
        time_to_scroll = thread_num/scrolls

        result = {
            'article_height': article_height,
            'scroll_down': int(scroll_down),
            'scrolls': scrolls,
            'time_to_scroll': time_to_scroll + time_to_scroll/5,
            'thread_num': thread_num
        }

        return result

    def determine_except(div_height, div_text):

        article_text = div_text
        num_to_multiply = math.ceil(len(article_text) / 1500)
        article_height = div_height
        scroll_down = 700.0/2
        scrolls = math.ceil(article_height/scroll_down)
        
        total_time = 60 * num_to_multiply

        time_to_scroll = (60 * num_to_multiply)/scrolls
        
        result = {
            'article_height': article_height,
            'scroll_down': int(scroll_down),
            'scrolls': scrolls,
            'time_to_scroll': time_to_scroll,
            'total_time': total_time,
            'num_to_multiply': num_to_multiply
        }

        return result