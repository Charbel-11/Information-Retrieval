#pragma once
#include <fstream>
#include <algorithm>
#include <vector>
#include <unordered_map>
#include <string>
using namespace std;

struct InvertedIndexReader {
	string path;
	int maxID = 4534;

	InvertedIndexReader(string _path = ".");

	//Returns a map term->postingList 
	unordered_map<string, vector<int>> getPostingLists() const;

	//Gets the documents in order; so res[2] returns the path of the document with ID 2
	vector<string> getDocPaths();
};