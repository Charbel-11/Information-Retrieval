#include "InvertedIndexReader.h";

InvertedIndexReader::InvertedIndexReader(string _path) {
	path = _path;
}

//Posting list format:
//term: freqID ID1, ID2, ..., IDn
unordered_map<string, vector<int>> InvertedIndexReader::getPostingLists() const {
	ifstream ifs(path + "\\Inverted Indexes.txt");
	unordered_map<string, vector<int>> res;

	while (true) {
		string curWord; ifs >> curWord;
		if (ifs.fail()) { break; }
		curWord.pop_back();

		vector<int> curID;
		int n; ifs >> n;
		for (int i = 0; i < n; i++) {
			string curS; ifs >> curS;
			if (curS.back() == ',') { curS.pop_back(); }
			curID.push_back(stoi(curS));
		}

		res[curWord] = curID;
	}

	ifs.close();
	return move(res);
}

//Get the documents in order; so res[2] returns the path of the document with ID 2
vector<string> InvertedIndexReader::getDocPaths() {
	ifstream ifs(path + "\\Document Order.txt");
	vector<string> res;
	while (true) {
		string cur;	getline(ifs, cur);
		if (ifs.fail()) { break; }
		res.push_back(cur);
	}
	ifs.close();
	maxID = (int)res.size() - 1;
	return move(res);
}