#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <set>
#include <algorithm>

class ContextFreeGrammar {

    int n;
    std :: string line;

    std :: vector <std :: string> N;
    std :: vector <std :: string> T;
    std :: vector <std :: vector<std :: string>> P;

    std :: set <std :: string> solution;
    std :: set <std :: string> repetitions;

    std :: ifstream in;
    std :: ofstream out;

public:

    int number_of_words() {
        return solution.size();
    }

    void close() {
        in.close();
        out.close();
        exit(1);
    }

    void check_duplicate(std :: vector <std :: string> v, std :: string w, char letter) {
        if (std :: find(v.begin(), v.end(), w) != v.end()) {
                std :: cerr << "Duplicate found in " << letter << ".\n";
                close();
            }
    }

    void check_uppercase(char w) {
        if ((w > 'Z' || w < 'A') && w != ',') {
            std :: cerr << "N should have only uppercase letters.\n";
            close();
        }
    }

    void check_lowercase(char w) {
        if ((w > 'z' || w < 'a') && w != ',') {
            std :: cerr << "T should have only lowercase letters.\n";
            close();
        }
    }

    void check_case(char letter, char w) {
        if (letter == 'N')
            check_uppercase(w);
        else if (letter == 'T');
            ///check_lowercase(w);
    }

    void check_eof(char letter) {
        if (in.eof()) {
            std :: cerr << "Lines missing in input (" << letter << ").\n";
            close();
        }
    }

    void check_missing_symbols(char letter) {
        if (line[0] != letter) {
            std :: cerr << letter << " is eronated (maybe '" << letter << "' missing / in the wrong place?).\n";
            close();
        }
        if (line[2] != '{') {
            std :: cerr << letter << " is missing '{'.\n";
            close();
        }

        if (line[line.size()-1] != '}') {
            std :: cerr << letter << " is missing '}'.\n";
            close();
        }

        if (line[1] != '=') {
            std :: cerr << letter << " is eronated (maybe '=' missing / in the wrong place?).\n";
            close();
        }
    }

    void check_projections(char w) {
            if (isupper(w) && std :: count(N.begin(), N.end(), std :: string(1, w)) == 0) {
             std :: cerr << "Unknown terminal in " << line.substr(0, line.find('|')) << ".\n";
             close();
        }
        else if(!isupper(w) && std :: count(T.begin(), T.end(), std :: string(1, w)) == 0) {
            std :: cerr << "Unknown symbol in " << line.substr(0, line.find('|')) << ".\n";
            close();
        }
    }

    void read_grammar(std :: vector <std :: string> &v, char letter) {
        std :: string currentChar;
        while(line == "" && !in.eof())
            getline(in, line);

        check_eof(letter);

        line.erase(remove(line.begin(), line.end(), ' '), line.end());

        check_missing_symbols(letter);

        line = line.substr(3, line.size() - 4) + ",";

        while (line.find(',') != -1) {
            currentChar = line[0];

            check_duplicate(v, currentChar, letter);

            check_case(letter, line[0]);

            v.push_back(currentChar);

            line = line.substr(line.find(',') + 1);
        }
    }

    void read_projects(std :: vector <std :: vector <std:: string>> &v) {
        std :: vector <std :: string> toAppend;

        for (int i = 0; i < N.size(); ++i) {
            while (line == "" && !in.eof())
                getline(in, line);

            line.erase(remove(line.begin(), line.end(), ' '), line.end());

            if (N.at(i) != std :: string(1, line[0]) || line.substr(3).size() == 0) {
                if (line[1] != '-' || line[2] != '>' || line.substr(3).size() == 0) {
                    std :: cerr << "Either missing projection " << N.at(i) << " or invalid format.\n";
                }
                else
                    std :: cerr << "The order of the projections do not match N (" << line[0] << " should be " << N.at(i) << ").\n";
                close();
            }

            if (line[1] != '-' || line[2] != '>') {
                std :: cerr << "Invalid format for projection " << line[0] << ".\n";
                close();
            }

            line = line.substr(3) + "|";

            while (line.find('|') != -1) {
                for (char s : line.substr(0, line.find('|')))
                    check_projections(s);
                toAppend.push_back(line.substr(0, line.find('|')));
                line = line.substr(line.find('|') + 1, line.size());
            }
            v.push_back(toAppend);
            toAppend.clear();
        }
    }

    void read_value(int &n) {
        while (line == "" && !in.eof())
            getline(in, line);

        line.erase(remove(line.begin(), line.end(), ' '), line.end());

        if (line[0] != 'n' || line[1] != '=') {
            std :: cerr << "Wrong input for the number.\n";
            close();
        }

        line = line.substr(line.find('=') + 1);

        for (char s : line)
            if (s < '0' || s > '9') {
                std :: cerr << "Number contains other symbols than digits.\n";
                close();
            }

        try {
            n = std :: stoi(line);
        }
        catch (std :: invalid_argument) {
            std :: cerr << "Wrong format for the number.\n";
            close();
        }
    }

    ContextFreeGrammar(std :: string input, std :: string output) {

        in.open(input);
        out.open(output);

        std :: string line, projection, number = "";
        std :: vector <std :: string> current;

        read_grammar(N, 'N');
        read_grammar(T, 'T');
        read_projects(P);
        read_value(n);

    }

    ~ContextFreeGrammar() {
        N.clear();
        N.shrink_to_fit();

        T.clear();
        T.shrink_to_fit();

        P.clear();
        P.shrink_to_fit();

        solution.clear();

        repetitions.clear();

        in.close();
        out.close();
    }

    void reccursion(std :: string S) {
        if (S.find("&") != -1 && S.size() > 1)
            S.erase(std :: remove(S.begin(), S.end(), '&'), S.end());
        size_t upperLetters = count_if(S.begin(), S.end(), [] (unsigned char ch) { return isupper(ch); });
        int position, index, self;
        if (upperLetters > 0) {
            repetitions.insert(S);
            if (S.size() - 1 <= n) {
                std :: string aux = S;
                for (char c : S)
                    if (isupper(c)) {
                        position = aux.find(c);
                        index = std :: distance(N.begin(), std :: find(N.begin(), N.end(), std :: string(1, c)));
                        if (S.size() == 1)
                            self = 1;
                        else
                            self = 0;
                        for (register int i = self; i < P[index].size(); ++i) {
                            aux.replace(position, 1, P[index][i]);
                            if (repetitions.count(aux) == 0) {
                                repetitions.insert(aux);
                                reccursion(aux);
                            }
                            aux = S;
                        }
                    }
            }
        }
        else
            if (S.size() <= n)
                solution.insert(S);
    }

    void solve() {
        if (n != 0)
            for (register int i = 0; i < P[0].size(); ++i)
                    reccursion(P[0][i]);
    }

    void print() {
        for (auto it = solution.begin(); it != solution.end();) {
            out << *it;
            if (++it != solution.end())
                out << "\n";
        }
    }

};

int main(int argc, char** argv) {

    if (argc < 3) {
        std :: cerr << "Usage: input_filename output_filename.\n";
        exit(1);
    }

    ContextFreeGrammar *G = new ContextFreeGrammar(argv[1], argv[2]);

    G -> solve();
    G -> print();

    int result = G -> number_of_words();

    std :: cerr << "Succes - " << result << " word";

    if (result > 1)
        std :: cerr << "s";

    std :: cout << " created.\n";

    delete G;

    return 0;
}
