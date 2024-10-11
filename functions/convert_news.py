import openai as client
import json
import logging
    
# JSON 파일 불러오기
with open('scored_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# score에 대해 가장 가까운 텍스트와 점수를 찾는 함수 정의
def find_closest_text(score, data):
    closest = min(data, key=lambda x: abs(x['score'] - score))
    return closest

# 주어진 score와 5% 높고 낮은 점수에 대해 가장 가까운 텍스트와 점수를 출력하는 함수
def get_closest_texts(score):
    original = find_closest_text(score, data)
    higher_score = score * 1.10
    lower_score = score * 0.90

    higher = find_closest_text(higher_score, data)
    lower = find_closest_text(lower_score, data)

    return {
        'original': original,
        'higher_10_percent': higher,
        'lower_10_percent': lower
    }

def convert_news_gpt(bases, score, text):
    base, higher, lower = bases['original'], bases['higher_10_percent'], bases['lower_10_percent']
        
    prompt = f"""
              당신은 문해력 측정의 최고 수준 알고리즘입니다. 
              당신은 사용자의 문해력 score에 맞게 주어진 기사를 이해하기 쉽게 또는 어렵게 변형시켜야 합니다. 이때, 낮은 score는 이해하기 쉬움을 의미합니다.
              
              문해력의 평가기준은 다음과 같습니다.
              
              [주어진 텍스트에 대해 이해의 난이도를 평가하세요. 이해의 난이도 점수는 독자가 해당 텍스트의 내용, 의도, 구조를 이해하는 데 얼마나 많은 노력이 필요한지를 측정합니다. 평가 시 다음 기준을 고려해 주십시오:

               이해 용이성 (Ease of Comprehension): 텍스트의 핵심 내용을 이해하는 데 얼마나 쉬운지 평가합니다. 독자가 주요 아이디어나 메시지를 빠르게 파악할 수 있는지 고려하십시오.
               논리적 연결성 (Logical Cohesion): 텍스트의 아이디어와 문장이 얼마나 논리적이고 일관되게 연결되어 있는지 평가합니다. 문장 간의 흐름과 전환이 자연스러운지 확인하세요.
               어휘 난이도 (Vocabulary Difficulty): 사용된 어휘가 독자에게 얼마나 이해하기 쉬운지 평가합니다. 전문 용어나 복잡한 단어가 과도하게 사용되었는지 고려하십시오.
               구문 구조 (Syntactic Complexity): 문장의 구조가 얼마나 복잡하거나 단순한지 평가합니다. 복잡한 문장 구조가 독자의 이해를 방해하지 않는지 중점적으로 봅니다.

               평가 척도
               0에서 100까지의 점수로 평가하며, 0은 매우 쉬운 이해 난이도를, 100은 매우 어려운 이해 난이도를 의미합니다.

               0-20: 이해 난이도가 매우 낮아, 독자가 텍스트를 즉각적으로 쉽게 이해할 수 있음.
               30-40: 이해 난이도가 낮아, 대부분의 독자가 텍스트를 큰 어려움 없이 이해할 수 있음.
               50-60: 이해 난이도가 중간 수준으로, 독자가 텍스트를 이해하는 데 약간의 노력이 필요함.
               70-80: 이해 난이도가 높은 편이며, 독자가 텍스트를 이해하기 위해 상당한 노력이 필요함.
               90-100: 이해 난이도가 매우 높아, 독자가 텍스트를 완전히 이해하기 위해 많은 노력이 필요함.

               제공된 텍스트는 다음과 같습니다. 일반적인 성인 남성이 적당히 이해할 수 있는 문장의 점수는 50입니다.]
               
              아래에 제공된 리스트는 당신이 예시로 사용할 [문해력 score : 해당 text] 예시입니다.
              ------------------------------------
              {base['score']}: {base['text']}
              {higher['score']}: {higher['text']}
              {lower['score']}: {lower['text']}
              ------------------------------------
              
              이제 제가 제공한 사용자의 score에 맞게 아래 제시된 기사를 변형시켜주세요.
              ------------------------------------
              사용자의 문해력 score: {score}
              변경한 text: {text}
              
              오직 변경된 text만을 출력해주세요. 다른 어떠한 것도 출력되어서는 안됩니다.
              """
    
    while True:
        try:
            response = client.chat.completions.create(
                model='gpt-4o-mini',
                messages=[{"role": "system", "content": prompt}],
                temperature=1
            )
            break
            
        except ValueError:
            logging.exception("message")
            continue
    
    return response.choices[0].message.content

def convert_news(score, text):
    return convert_news_gpt(get_closest_texts(score), score, text)