#include <iostream>
#include <omp.h>

using namespace std;

// Merge function to combine two sorted halves
void merge(int arr[], int low, int mid, int high) {
    // Create arrays of left and right partitions
    int n1 = mid - low + 1;
    int n2 = high - mid;

    // Using dynamic allocation for standard C++ compliance
    int* left = new int[n1];
    int* right = new int[n2];
    
    // Copy all left elements
    for (int i = 0; i < n1; i++) left[i] = arr[low + i];
    
    // Copy all right elements
    for (int j = 0; j < n2; j++) right[j] = arr[mid + 1 + j];
    
    // Compare and place elements
    int i = 0, j = 0, k = low;

    while (i < n1 && j < n2) {
        if (left[i] <= right[j]){
            arr[k] = left[i];
            i++;
        } 
        else {
            arr[k] = right[j];
            j++;
        }
        k++;
    }

    // If any elements are left out in the left array
    while (i < n1) {
        arr[k] = left[i];
        i++;
        k++;
    }

    // If any elements are left out in the right array
    while (j < n2) {
        arr[k] = right[j];
        j++;
        k++;
    }

    // Clean up memory
    delete[] left;
    delete[] right;
}

// Parallel Merge Sort utilizing OpenMP sections
void parallelMergeSort(int arr[], int low, int high) {
    if (low < high) {
        int mid = (low + high) / 2;

        // Creates a team of threads and divides the sections block among them. 
        // Each section inside runs on a different thread simultaneously.
        #pragma omp parallel sections
        {
            #pragma omp section
            {
                parallelMergeSort(arr, low, mid);
            }

            #pragma omp section
            {
                parallelMergeSort(arr, mid + 1, high);
            }
        }
        // Implicit barrier here: threads join before moving to the merge step
        
        merge(arr, low, mid, high);
    }
}

// Sequential Merge Sort
void mergeSort(int arr[], int low, int high) {
    if (low < high) {
        int mid = (low + high) / 2;
        mergeSort(arr, low, mid);
        mergeSort(arr, mid + 1, high);
        merge(arr, low, mid, high);
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

    // Use dynamic arrays based on user input
    int* arr = new int[n];
    int* backup = new int[n];

    // 2. Get the actual numbers from the user
    cout << "Enter " << n << " numbers separated by spaces: ";
    for(int i = 0; i < n; i++) {
        cin >> arr[i];
        backup[i] = arr[i]; // Save a copy for the parallel test
    }
    
    double start_time, end_time; 

    // --- SEQUENTIAL RUN ---
    cout << "\n--- Sequential Merge Sort ---\n";
    start_time = omp_get_wtime(); 
    mergeSort(arr, 0, n - 1);
    end_time = omp_get_wtime(); 
    
    cout << "Sorted Array: ";
    printArray(arr, n);
    cout << "Sequential Time taken : " << end_time - start_time << " seconds\n";

    // 3. Reset the array back to the user's original input
    for(int i = 0; i < n; i++) {
        arr[i] = backup[i];
    }
    
    // --- PARALLEL RUN ---
    cout << "\n--- Parallel Merge Sort ---\n";
    start_time = omp_get_wtime(); 
    parallelMergeSort(arr, 0, n - 1);
    end_time = omp_get_wtime(); 
    
    cout << "Sorted Array: ";
    printArray(arr, n);
    cout << "Parallel Time taken   : " << end_time - start_time << " seconds\n";
    
    // 4. Clean up memory
    delete[] arr;
    delete[] backup;

    return 0;
}
