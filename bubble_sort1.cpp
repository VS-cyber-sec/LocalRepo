#include <iostream>
#include <omp.h>

using namespace std;

// Sequential Bubble Sort
void bubble(int array[], int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (array[j] > array[j + 1]) {
                swap(array[j], array[j + 1]);
            }
        }
    }
}

// Parallel Bubble Sort (Odd-Even Transposition Sort)
void pBubble(int array[], int n) {
    for (int i = 0; i < n; ++i) {
        
        // Phase 1: Sort odd-indexed numbers
        #pragma omp parallel for
        for (int j = 1; j < n; j += 2) {
            if (array[j] < array[j - 1]) {
                swap(array[j], array[j - 1]);
            }
        }
        // Implicit barrier here: all threads wait until odd phase is done

        // Phase 2: Sort even-indexed numbers
        #pragma omp parallel for
        for (int j = 2; j < n; j += 2) {
            if (array[j] < array[j - 1]) {
                swap(array[j], array[j - 1]);
            }
        }
        // Implicit barrier here: all threads wait until even phase is done
    }
}

// Utility function to print the array
void printArray(int arr[], int n) {
    for (int i = 0; i < n; i++) {
        cout << arr[i] << " ";
    }
    cout << "\n";
}

int main() {
    int n;
    
    // 1. Get the size of the array from the user
    cout << "Enter the number of elements: ";
    cin >> n;

    // Using dynamic arrays so the size 'n' can be decided at runtime
    int* arr = new int[n];
    int* backup = new int[n];

    // 2. Get the actual numbers from the user
    cout << "Enter " << n << " numbers separated by spaces: ";
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
        backup[i] = arr[i]; // Save a copy for the parallel test
    }
    
    double start_time, end_time;

    // --- SEQUENTIAL RUN ---
    cout << "\n--- Sequential Bubble Sort ---\n";
    start_time = omp_get_wtime();
    bubble(arr, n);
    end_time = omp_get_wtime();     
    
    cout << "Sorted Array: ";
    printArray(arr, n);
    cout << "Sequential Time taken : " << end_time - start_time << " seconds.\n";
    
    
    // 3. Reset the array back to the user's original input
    for (int i = 0; i < n; i++) {
        arr[i] = backup[i];
    }
    
    
    // --- PARALLEL RUN ---
    cout << "\n--- Parallel Bubble Sort ---\n";
    start_time = omp_get_wtime();
    pBubble(arr, n);
    end_time = omp_get_wtime();     
    
    cout << "Sorted Array: ";
    printArray(arr, n);
    cout << "Parallel Time taken   : " << end_time - start_time << " seconds.\n";

    // 4. Clean up memory
    delete[] arr;
    delete[] backup;

    return 0;
}
