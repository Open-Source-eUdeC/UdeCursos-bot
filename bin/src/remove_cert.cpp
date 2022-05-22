#include <bits/stdc++.h>
#include <regex>
using namespace std;

const regex regex_("  \"[a-zA-z0-9]+\": \\{");

void replaceData(string &line, string type, string name, string date) {
    map<string, string> data = {
        {"&", string(1,34)},
        {"[TYPE]", type},
        {"[NAME]", name},
        {"[DATE]", date},
    };
    for(auto &k: data){
        int pos = line.find(k.first);
        while(pos != string::npos){
            string aux_line = line.substr(pos + k.first.size());
            line.replace(line.begin() + pos, line.end(), k.second);
            line += aux_line;
            pos = line.find(k.first);
        }
    }
}
void removeByDate(vector<string> &file_lines, string parent, string type, string name, string date){
    string line_to_delete = "      { &type&: &[TYPE]&, &name&: &[NAME]&, &date&: &[DATE]& }";
    replaceData(line_to_delete, type, name, date);
    bool found_parent = false;
    for(auto &l : file_lines){
        if(regex_match(l, regex_)){
            string parent_line = l.substr(l.find("\"") + 1, l.find("\"", l.find("\"") + 1) - l.find("\"") - 1);
            found_parent = !parent.compare(parent_line);
        }
        if(!l.compare(line_to_delete) && found_parent) {
            if((*(&l-1)).find("[") == string::npos) {
                (*(&l-1)) = (*(&l-1)).substr(0, (*(&l-1)).size() - 1);
            } // fix trailing comma
        }
        if((!l.compare(line_to_delete) || !l.compare(line_to_delete + ",")) && found_parent) {
            file_lines.erase(find(file_lines.begin(), file_lines.end(), l));
        }
    }
}
int main(int argc, char *argv[]) { // ./remove_cert gen2022 Cert Calculo III 2020-09-03
    vector<string> args(argv, argv+argc);
    const string file_location = "data/certs.json", parent = args[1];
    string name = "";
	for (unsigned i=3; i < args.size()- 1; ++i) name += args[i] + (i + 1 == args.size()- 1 ? "" : " ");
    fstream file(file_location, ios::in);
    vector<string> file_lines;
    if(file.is_open()) {
        string file_line;
        while(getline(file, file_line)) file_lines.push_back(file_line);
        file.close();
        removeByDate(file_lines, parent, args[2], name, args[args.size() - 1]);
        fstream file(file_location, ios::out);
        for(auto &l : file_lines) file << l << endl;
        file.close();
	} else {
		cout << "An error has occured while opening the file :/\n";
	}
    return 0;
}