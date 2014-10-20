
public class A1
{
    public static void insertionSort(int[] arr) {
        for (int j = 1; j < arr.length; j++) {
            int key = arr[j];
            int i = j - 1;
            while (i >= 0 && arr[i] > key) {
                int temp = arr[i + 1];
                arr[i + 1] = arr[i];
                arr[i] = temp;
                
                i -= 1;
            }
        }
    }
    
    public static int[] addBinary(int[] num1, int[] num2) {
        int[] c = new int[4];
        return c;
    }
    
    public static void printArray(int[] arr) {
        for (int i = 0; i < arr.length; i++) {
            System.out.println(arr[i]);
        }
        System.out.println(" ");
    }
    
    public static void main(String [] args) {
        int[] test = {1, 4, 5, 2, 3, -1};
        printArray(test);
        printArray(addBinary(test, test));
    }
}
