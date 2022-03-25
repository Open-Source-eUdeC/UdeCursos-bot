#include <iostream>
#include <fstream>
#include <string>
#include <vector>

using namespace std;

string replaceQuotes(string a) {
	unsigned short int i = 0;
	while (i < a.size()) {
		if (a[i] == '&') {
			a[i] = 34; // charify(34) == "
		}
		++i;
	}
	return a;
}

bool isSubstringOf(string sub, string whole) {
	bool firstMatches = false;
	unsigned short int match;
	for (unsigned short int i=0; i<whole.size(); ++i) {
		if (firstMatches) {
			if (match >= sub.size() || (match+1 == sub.size() && i+1 == whole.size())) {
				return true;
			}
			if (whole[i] != sub[match]) {
				firstMatches = false;
			}
			match++;
		}
		if (whole[i] == sub[0] && !firstMatches) {
			if (sub.size() == 1) return true;
			firstMatches = true;
			match = 1;
		}
	}
	return false;
}
void printVector(vector<string> vec) {
	for (short i=0;i<vec.size();++i) {
		cout << vec[i] << " ";
	}
	cout << endl;
}

int main(int argc, char *argv[]) { // ./bin/insert_cert gen2020 <Cert/Test> Calculo III 2020-09-23
	string line;
	bool genMatches = false;
	bool next = false;
	vector <string> args(argv, argv+argc);
	string altered_file = "";
	bool altered = false;
	const string file_location = "data/certs.json";

	string type = args[2];
	string line_to_insert = "      { &type&: &";
	line_to_insert += type + "&, ";
	line_to_insert += "&name&: &";
	for (unsigned i=3; i < args.size()- 1; ++i) {
		line_to_insert += args[i] + " ";
	}
	line_to_insert.pop_back(); // deletes the last space
	line_to_insert += "&, &date&: &";
	line_to_insert += args[args.size()- 1];
	line_to_insert += "& }";
	line_to_insert = replaceQuotes(line_to_insert);


	fstream file(file_location, ios::in); //Runs through the file to find out where it should insert the line
	if (file.is_open()) {
		while (getline (file, line)) {
			if (next) {	// Reviews if should write the comma, cause the finish of the json attribute
				if (isSubstringOf("name", line)) line_to_insert += ",";
				line_to_insert += "\n";
				altered_file += line_to_insert;
				next = false;
			}
			altered_file += line + "\n";
			if (isSubstringOf(args[1], line) && !altered) { // finds rigth gen
				genMatches = true;
			}
			if (genMatches && !altered) {
				if (isSubstringOf("certs", line)) { // Looks for "certs": {
					altered = true;
					next = true;
				}
			}
		}
		
		altered_file.pop_back(); // Removes the final "\n"
		file.close();
		fstream file(file_location, ios::out); // Opens the file in write mode
		file << altered_file;
		file.close();
	} else {
		cout << "An error has occured while opening the file :/\n";
	}

}
