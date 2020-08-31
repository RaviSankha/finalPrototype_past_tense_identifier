from flask import Flask,render_template,request,jsonify
import nltk

# I worked on this code by myself(no team)

# for developing the code the following tutorials and web sites were referred 
# https://www.nltk.org/book/ch05.html
# https://stackoverflow.com/questions/19966345/identifying-verb-tenses-in-python/19982051
# https://stackoverflow.com/questions/73663/how-to-terminate-a-python-script
# https://www.w3schools.com/python/python_functions.asp
# https://pypi.org/project/termcolor/
# https://www.tutorialspoint.com/How-to-change-text-font-in-HTML#:~:text=To%20change%20the%20text%20font,%2C%20font%2Dstyle%2C%20etc.
# https://www.pitt.edu/~naraehan/python3/split_join.html
# https://pythonprogramming.net/jquery-flask-tutorial/
# https://www.freecodecamp.org/news/html-background-color-tutorial-how-to-change-a-div-background-color-explained-with-code-examples/
# https://www.w3schools.com/howto/howto_css_style_hr.asp

app = Flask(__name__)

@app.route('/prototype/')
def prototype():
	return render_template('prototype.html')


@app.route('/background_process')
def background_process():
    sentence = request.args.get('sentenceInput', 0, type=str)
        
    #if the user does not enter a sentence but click on the button    
    if (sentence== "" or sentence==None) :
        return jsonify(result2="",result3="Please write a sentence...",result4="",result1="") 

    tokens=nltk.word_tokenize(sentence)
    #to store all the tags of terms
    tags=[pos for (word, pos) in nltk.pos_tag(tokens)]
    #to store instances of past tense in the sentence
    pastVerbs = [word for (word, pos) in nltk.pos_tag(tokens) if(pos == 'VBD')]
    #to obatin the number of simple past verbs
    count=tags.count('VBD')
    #if there are no simple past verbs in the sentence
    if (count==0):
        return jsonify(result2=sentence,result3="",result4="",result1="The sentence is not in past simple tense.") 
       

	#if there is only one simple past verb in the sentence
    #the previous tools falsely detected past progressive,past perfect simple and past perfect progressive tenses as simple past tense 
    #this part was developed to avoid and minimize those defects    
    if (count==1):
        #to check whether present participles are included in the sentence(with the occurance of was or were)
        identifier=0
        if(pastVerbs[0]=="was" or pastVerbs[0]=="were"):
            for term in tags:
                if(term == "VBG"):
                    identifier=1
                    break
            
        preParCount=identifier
        #the tool detects that this sentence is not in past simple tense(may be in past progressive tense)
        if(preParCount==1):
            return jsonify(result2=sentence,result3="",result4="",result1="The sentence is not in past simple tense.") 
        
        #to check whether past participles are included in the sentence(with the occurance of had)    
        identifier1=0
        if(pastVerbs[0]=="had"):  
             for term in tags:
                 if(term == "VBN"):
                     identifier1=1
                     break
        pastParCount=identifier1
        #the tool detects that this sentence is not in past simple tense(may be in past perfect simple tense or past perfect progressive tense)
        if(pastParCount==1):
            return jsonify(result2=sentence,result3="",result4="",result1="The sentence is not in past simple tense.") 
    
    #to split the sentence which is in past simple tense
    splittedSen=sentence.split(pastVerbs[0])
    return jsonify(result2=splittedSen[0],result3=splittedSen[1],result4=pastVerbs[0],result1="The sentence is in past simple tense.") 
    
      
if __name__ == '__main__':
    app.run()