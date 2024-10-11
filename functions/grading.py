import openai as client
import json
import logging

def essay_grading(text, ques, ans):
        
    prompt = f"""
              당신은 최고수준의 뉴스 이해 및 강의 알고리즘입니다.
              당신은 사용자의 논설문을 뉴스와 대조하여 채점하고자 합니다.
              
              채점은 상, 중, 하로만 이루어집니다.  근거와 논리를 잘 들어 주장한 경우 상, 근거가 있지만 논리가 부족하거나, 논리는 있지만 근거가 부족한 경우 중, 근거와 논리가 모두 없거나 잘못된 근거를 들고 있는 경우 하로 채점해야 합니다.
              사용자의 문장은 2~3문장 사이로 이루어집니다. 따라서 해당 문장에서 할 수 있는 충분한 논설을 했으면 잘 평가해주시면 됩니다. 모든 근거는 제공된 뉴스에서 발췌되어야 합니다. 그렇지 않은 경우, 해당 근거는 거짓이며 이는 강력한 감점 사유입니다.
              
              뉴스: {text}
              문제: {ques}
              사용자의 답안: {ans}
              
              오직 상, 중, 하의 한 단어로만 출력하세요. 그 밑에는 이유를 출력하세요. 해당 이유는 제공된 뉴스에 근거하여 설명되어야 합니다. 그 외에는 절대 출력하지 마세요.
              """
    
    while True:
        try:
            response = client.chat.completions.create(
                model='gpt-4o',
                messages=[{"role": "system", "content": prompt}],
                temperature=0.3
            )
            break
            
        except ValueError:
            logging.exception("message")
            continue
    
    return response.choices[0].message.content

def grading(ans, qa, text):
    score = 0
    if ans[0] == qa[0]['answer']:
        score += 1
    if ans[1] == qa[1]['answer']:
        score += 1
        
    res = essay_grading(text, qa[2]['question'], ans[2])
    
    res_list = res.split('\n')
    
    essay_res = res_list[0]
    essay_solution = ''.join(res_list[1:])
    
    print(essay_res)
    
    if '상' in essay_res:
        score += 2
    elif '중' in essay_res:
        score += 0.5
    else:
        score -= 1
        
    return score, essay_solution

