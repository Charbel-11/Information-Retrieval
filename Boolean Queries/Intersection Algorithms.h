#pragma once
#include <algorithm>
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