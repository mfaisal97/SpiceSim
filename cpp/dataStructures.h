#include <vector>
#include <string>

using namespace std;

//! To DO:
//1) assume only y is the output
//2) assume that the expression does not have negation on an expresssion (parentheses)
//3) 


//prototype
class spiceOperand;
class simpleOperand;
class expressionOperand;



////////////////////////////////////////
/////////////   Helpers    /////////////
////////////////////////////////////////
vector<string> splitString(string str, char del){
    

    vector<string> splitted;
    int start = 0;
    for(int i = 0; i < str.size();i++){
        if (str[i] == del){
            splitted.push_back(str.substr(start, i-start));
            start = i + 1;
        }
    }

    return splitted;
}





////////////////////////////////////////
/////////////   Operands    ////////////
////////////////////////////////////////



////////////////////////////////////////
/////////////   Operators    ///////////
////////////////////////////////////////
enum spiceOperatorType{notOperand, andOperand, orOperand, noOperator};

class spiceOperator{
private:
    spiceOperatorType operatorType;
    
public:
    spiceOperator(){

    }

    ~spiceOperator(){
        
    }
};




////////////////////////////////////////
/////////////   Operands    ////////////
////////////////////////////////////////
class expressionOperand(){
private:
    string name;
    vector <expressionOperand> operands;
    spiceOperator op;

    bool isSimpleOperand;
    string simpleOperand;

public:
    expressionOperand(string expr){
        if(expr.find("&") != string::npos){

        }else if ()
    }

}

////////////////////////////////////////
////////////   Transistors    //////////
////////////////////////////////////////