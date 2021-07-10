#include <chrono>
#include <fstream>
#include <iostream>
#include "Intersection Algorithms.h";

void create26Folders() {
	ifstream ifs("Inverted Indexes.txt");
	ofstream ofs("DictionaryByLetter\\a.txt");
	char curC = 'a';

	vector<int> docIDs;
	while (true) {
		string curWord; ifs >> curWord;
		if (ifs.fail()) { break; }

		if (curWord[0] != curC) {
			for (auto& x : docIDs) { ofs << x << '\n'; }
			curC = curWord[0]; docIDs.clear();
			ofs = ofstream(string("DictionaryByLetter\\") + curC + ".txt");
		}

		vector<int> curID;
		int n; ifs >> n;
		for (int i = 0; i < n; i++) {
			string curS; ifs >> curS;
			if (curS.back() == ',') { curS.pop_back(); }
			curID.push_back(stoi(curS));
		}

		vector<int> res(curID.size() + docIDs.size());
		merge(curID.begin(), curID.end(), docIDs.begin(), docIDs.end(), res.begin());
		res.erase(unique(res.begin(), res.end()), res.end());
		swap(docIDs, res);
	}

	for (auto& x : docIDs) { ofs << x << '\n'; }
}

//Tests the runtime of the different intersection algorithms
void intersectAllPairs() {
	vector<vector<int>> lists(26, vector<int>());

	auto start = chrono::high_resolution_clock::now();
	for (int i = 0; i < 26; i++) {
		char c = 'a' + i;
		ifstream ifs(string("DictionaryByLetter\\") + c + ".txt");
		while (true) {
			int cur; ifs >> cur;
			if (ifs.fail()) { break; }
			lists[i].push_back(cur);
		}
	}
	auto stop = chrono::high_resolution_clock::now();
	auto readDuration = chrono::duration_cast<chrono::microseconds>(stop - start);

	ll totalLen = 0;
	ll runtimeAlgo1 = 0, runtimeAlgo2 = 0;
	for (int i = 0; i < 26; i++) {
		for (int j = i + 1; j < 26; j++) {
			totalLen += lists[i].size() + lists[j].size();

			start = chrono::high_resolution_clock::now();
			vector<int> res1 = intersectOld(lists[i], lists[j]);
			stop = chrono::high_resolution_clock::now();
			auto duration = chrono::duration_cast<chrono::microseconds>(stop - start);
			runtimeAlgo1 += duration.count();

			start = chrono::high_resolution_clock::now();
			vector<int> res2 = getIntersectionHybrid(lists[i], lists[j]);
			stop = chrono::high_resolution_clock::now();
			duration = chrono::duration_cast<chrono::microseconds>(stop - start);
			runtimeAlgo2 += duration.count();

			assert(res1 == res2);
		}
	}

	cout << "Rate to read the lists from disk: ";
	cout << totalLen * 1000000 / readDuration.count() << " elements/second" << '\n';

	cout << "Runtime of algos in microseconds: " << runtimeAlgo1 << " " << runtimeAlgo2 << '\n';
	cout << "Total elements processed by each algo: " << totalLen << '\n';

	cout << "Elements per second processed in the intersection algorithms: " << '\n';
	cout << "Old Algo: " << totalLen * 1000000 / runtimeAlgo1 << '\n';
	cout << "New Algo: " << totalLen * 1000000 / runtimeAlgo2 << '\n';
}

int main() {
	create26Folders();
	intersectAllPairs();
}