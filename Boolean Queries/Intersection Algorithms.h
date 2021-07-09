#include <fstream>
#include <iostream>
#include <algorithm>
#include <chrono>
#include <cassert>
#include <vector>
#include <string>
#include <list>
using namespace std;
typedef long long ll;

vector<int> intersectOld(vector<int>& a, vector<int>& b) {
	vector<int> res;
	int i = 0, j = 0;
	int n = a.size(), m = b.size();

	while (i < n && j < m) {
		if (a[i] == b[j]) { res.push_back(a[i]); i++; j++; }
		else if (a[i] < b[j]) { i++; }
		else { j++; }
	}

	return move(res);
}

//Algorithm based on Ricardo Baeza-Yates' and Alejandro Salinger's paper
//For n>=m, worst case: O(mlogn); Average case: O(mlog(n/m)) 
list<int> intersectNew(int lA, int rA, int lB, int rB, vector<int>& a, vector<int>& b) {
	if (lA > rA || lB > rB || a[lA] > b[rB] || b[lB] > a[rA]) { return list<int>(); }
	if (a.size() < b.size()) { swap(a, b); swap(lA, lB); swap(rA, rB); }

	int mid = (lB + rB) >> 1;
	int idxA = lower_bound(a.begin() + lA, a.begin() + rA + 1, b[mid]) - a.begin();
	bool midEqual = (a[idxA] == b[mid]);
	list<int> res = intersectNew(lA, idxA - 1, lB, mid - 1, a, b);
	if (midEqual) { res.push_back(b[mid]); }
	list<int> resR = intersectNew(idxA + midEqual, rA, mid + 1, rB, a, b);
	res.splice(res.end(), resR);
	return move(res);
}

vector<int> getIntersectionHybrid(vector<int>& a, vector<int>& b) {
	if (a.size() < b.size()) { swap(a, b); }
	int n = a.size(), m = b.size();
	if (m <= (n / log2((double)n))) { 
		list<int> res = intersectNew(0, n - 1, 0, m - 1, a, b);
		return vector<int>(res.begin(), res.end());
	}
	else { return intersectOld(a, b); }
}


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

void testALgorithms() {
	create26Folders();
	intersectAllPairs();
}