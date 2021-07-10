#include <fstream>
#include <iostream>
#include <algorithm>
#include <stack>
#include <vector>
#include <unordered_map>
#include <string>
#include "Intersection Algorithms.h";
#include "../Index Builder/InvertedIndexReader.h"
using namespace std;
typedef long long ll;

//Goal: Handle these queries
vector<string> queries = {
	"(graph AND (vector AND (NOT number)))",
	"((dynam AND program) OR ((NOT string) AND (subproblem AND array)))",
	"(search AND (ternari AND (NOT (binari OR full))))",
	"((tree OR graph) AND travers)",
	"((NOT (prime OR number)) AND tree)"
};

//Returns a OR b
vector<int> getUnion(const vector<int>& a, const vector<int>& b) {
	vector<int> res;
	int i = 0, j = 0;
	int n = a.size(), m = b.size();

	while (i < n && j < m) {
		if (a[i] == b[j]) { res.push_back(a[i]); i++; j++; }
		else if (a[i] < b[j]) { res.push_back(a[i]); i++; }
		else { res.push_back(b[j]); j++; }
	}

	while (i < n) { res.push_back(a[i++]); }
	while (j < m) { res.push_back(b[j++]); }

	return move(res);
}

//Returns a AND NOT b
vector<int> getIntersectionNot(const vector<int>& a, const vector<int>& b) {
	vector<int> res;
	int i = 0, j = 0;
	int n = a.size(), m = b.size();

	while (i < n && j < m) {
		if (a[i] < b[j]) { res.push_back(a[i]); i++; }
		else if (a[i] == b[j]) { i++; j++; }
		else { j++; }
	}
	while (i < n) { res.push_back(a[i++]); }

	return move(res);
}

//Gets all elements from 0 to maxID not in a
vector<int> reverseVector(const vector<int>& a, int maxID) {
	vector<int> res;
	int j = 0, n = a.size();
	for (int i = 0; i <= maxID; i++) {
		if (j < n && a[j] == i) { j++; continue; }
		res.push_back(i);
	}
	return move(res);
}

bool isNum(const string& s) {
	return s[0] >= '0' && s[0] <= '9';
}

vector<int> handleBooleanQuery(const string& q, unordered_map<string, vector<int>>& postingLists, int maxID) {
	stack<string> S;
	int n = q.size();
	vector<pair<vector<int>, bool>> interAns;

	for (int i = n - 1; i >= 0; i--) {
		if (q[i] == ' ') { continue; }
		if (q[i] == '(') {
			vector<string> curOp;
			while (S.top() != ")") {
				curOp.push_back(S.top());
				S.pop();
			}
			S.pop();

			if (curOp[0] == "NOT"){
				if (isNum(curOp[1])) {
					int idx = stoi(curOp[1]);
					interAns[idx].second = !interAns[idx].second;
					S.push(to_string(idx));
				}
				else {
					vector<int> curList = postingLists[curOp[1]];
					interAns.push_back({ curList, true });
					S.push(to_string(interAns.size() - 1));
				}
			}
			else {
				bool andOp = (curOp[1] == "AND");
				bool rev1 = false, rev2 = false, allRev = false;
				vector<int> v1, v2;
				if (isNum(curOp[0])) { 
					int idx = stoi(curOp[0]);
					v1 = interAns[idx].first;
					rev1 = interAns[idx].second;
				}
				else { v1 = postingLists[curOp[0]]; }
				if (isNum(curOp[2])) {
					int idx = stoi(curOp[2]);
					v2 = interAns[idx].first;
					rev2 = interAns[idx].second;
				}
				else { v2 = postingLists[curOp[2]]; }

				if (rev1 && rev2) { rev1 = rev2 = false; andOp = !andOp; allRev = true; }
				if (rev1 && !rev2) { swap(rev1, rev2); swap(v1, v2); }
				if (!rev1 && rev2 && !andOp) { andOp = true; swap(v1, v2); allRev = true; }

				vector<int> ans;
				if (!rev1 && !rev2 && !andOp) { ans = getUnion(v1, v2); }
				else if (!rev1 && !rev2 && andOp) { ans = getIntersectionHybrid(v1, v2); }
				else { ans = getIntersectionNot(v1, v2); }

				S.push(to_string(interAns.size()));
				interAns.push_back({ ans, allRev });
			}
		}
		else if (q[i] == ')') {
			S.push(")"); 
		}
		else {
			string cur = ""; int j = i;
			while (q[j] != ' ' && q[j] != '(') {
				cur.push_back(q[j]); j--;
			}
			reverse(cur.begin(), cur.end());
			S.push(cur); i = j + 1;
		}
	}
	
	vector<int> ans = interAns.back().first;
	if (interAns.back().second) { return move(reverseVector(ans, maxID)); }
	else { return move(ans); }
}

int main() {
	InvertedIndexReader reader;
	vector<string> docPaths = reader.getDocPaths();
	unordered_map<string, vector<int>> postingLists = reader.getPostingLists();

	for (int i = 0; i < 5; i++) {
		vector<int> ans = handleBooleanQuery(queries[i], postingLists, reader.maxID);
		for (auto& x : ans) { cout << docPaths[x] << '\n'; }
		cout << '\n' << '\n';
	}
}


/*
Algorithm overview:
Implementing the NOT by just getting a vector with all others element is inefficient
It defeats the purpose of having inverted indices rather than a term-document matrix.
So, instead, I kept track of a boolean which tells me if a particular list should be considered reversed.
Implemented AND, OR, NOT alone. Now we need to combine. AND and ORs are combined using the implemented function, just a matter of precedence.

For NOT, we will simplify our problem first:
NOT A AND NOT B is just NOT(A OR B) so we know how to do it
Similarly, NOT A OR NOT B is just NOT(A AND B)
NOT A AND B is equivalent to B AND NOT A (since AND is commutative)
NOT A OR B is equivalent to B OR NOT A

So, we still have to implement A AND NOT B and A OR NOT B.
A AND NOT B is easily implemented by changing A AND B a little.
We still have A OR NOT B.
The problem here is that it requires getting all the elements which aren't in B since they might be in the answer.
In other words, the answer could be much bigger than the size of A and the size of B, so that might blow off our complexity.
So, instead, we will say that A OR NOT B is equivalent to NOT(NOT A AND B) which we know how to deal with.
To explain why this works, the idea is that we first get the IDS for B AND NOT A which we know how to do linearly.
Then, we just set the reverse boolean of that vector to true rather than fetching all these other doc IDs.

In the end, if our resulting vector has that boolean true, we can just fetch all the other numbers.
This is fine as this is done at most once in our query.

Asymptotically, the complexity becomes (#doc IDs present in lists of queried words  * number of boolean operators + #doc IDs).
Since each binary operator sees a list which has at most all those doc IDs since we never get new ones.
Had we not used the boolean trick, it would have become O(#doc IDs * number of boolean operators)
Since each binary operator might have traversed all doc IDs.

For further explanation: A OR NOT A gives all docs but NOT(A AND NOT A) gives empty list with rev=true
And this is regardless of the size of A initially.
*/