#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// Function to sort an array
void sortArray(vector<int>& arr) {
    sort(arr.begin(), arr.end());
}

// Function to search for an element in the array
bool binarySearch(const vector<int>& arr, int target) {
    return binary_search(arr.begin(), arr.end(), target);
}

// Function to calculate the factorial of a number
int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

// Function to find the maximum element in an array
int findMax(const vector<int>& arr) {
    return *max_element(arr.begin(), arr.end());
}

// Function to display an array
void displayArray(const vector<int>& arr) {
    for (int num : arr) {
        cout << num << " ";
    }
    cout << endl;
}

// Main function
int main() {
    vector<int> numbers = {5, 3, 8, 1, 9, 4};

    cout << "Original Array: ";
    displayArray(numbers);

    sortArray(numbers);
    cout << "Sorted Array: ";
    displayArray(numbers);

    int target = 8;
    cout << "Searching for " << target << ": " 
         << (binarySearch(numbers, target) ? "Found" : "Not Found") << endl;

    int num = 5;
    cout << "Factorial of " << num << " is " << factorial(num) << endl;

    cout << "Maximum element in array: " << findMax(numbers) << endl;

    return 0;
}
