import streamlit as st
import matplotlib.pyplot as plt
import random
import time

st.set_page_config(page_title="DAA Sorting Game", layout="wide")

st.title("🎮 DAA Gaming Simulation - Advanced Sorting Visualizer")
st.write("VisuAlgo-style sorting animation using Streamlit")

st.sidebar.header("⚙️ Controls")

algorithm = st.sidebar.selectbox(
    "Choose Algorithm",
    ["Bubble Sort", "Selection Sort", "Insertion Sort"]
)

input_type = st.sidebar.radio("Input Type", ["Random Array", "Custom Array"])

size = st.sidebar.slider("Array Size", 5, 20, 10)
speed = st.sidebar.slider("Animation Speed", 0.1, 2.0, 0.5)

if input_type == "Custom Array":
    custom_input = st.sidebar.text_input(
        "Enter numbers separated by comma",
        "45, 12, 78, 23, 56, 10, 90"
    )
    try:
        arr = [int(x.strip()) for x in custom_input.split(",")]
    except:
        st.error("Please enter valid numbers like: 10, 20, 30")
        st.stop()
else:
    if "array" not in st.session_state or len(st.session_state.array) != size:
        st.session_state.array = [random.randint(10, 100) for _ in range(size)]

    if st.sidebar.button("🔄 Generate New Array"):
        st.session_state.array = [random.randint(10, 100) for _ in range(size)]

    arr = st.session_state.array.copy()

def draw_array(arr, highlight=[], sorted_part=[]):
    fig, ax = plt.subplots(figsize=(10, 4))

    colors = []
    for i in range(len(arr)):
        if i in sorted_part:
            colors.append("green")
        elif i in highlight:
            colors.append("red")
        else:
            colors.append("skyblue")

    ax.bar(range(len(arr)), arr, color=colors)
    ax.set_xticks(range(len(arr)))
    ax.set_xticklabels(arr)
    ax.set_title("Sorting Visualization")
    ax.set_xlabel("Array Index")
    ax.set_ylabel("Value")

    st.pyplot(fig)
    plt.close(fig)

def show_algorithm_info(algo):
    st.subheader("📘 Algorithm Explanation")

    if algo == "Bubble Sort":
        st.write("""
        Bubble Sort compares adjacent elements and swaps them if they are in the wrong order.
        After each pass, the largest element moves to its correct position at the end.
        """)
        pseudo = """
for i = 0 to n-1:
    for j = 0 to n-i-2:
        if arr[j] > arr[j+1]:
            swap arr[j] and arr[j+1]
        """

    elif algo == "Selection Sort":
        st.write("""
        Selection Sort finds the minimum element from the unsorted part and places it at the beginning.
        It repeats this process until the complete array is sorted.
        """)
        pseudo = """
for i = 0 to n-1:
    min_index = i
    for j = i+1 to n:
        if arr[j] < arr[min_index]:
            min_index = j
    swap arr[i] and arr[min_index]
        """

    else:
        st.write("""
        Insertion Sort picks one element at a time and inserts it into its correct position
        in the already sorted part of the array.
        """)
        pseudo = """
for i = 1 to n-1:
    key = arr[i]
    j = i - 1
    while j >= 0 and arr[j] > key:
        arr[j+1] = arr[j]
        j = j - 1
    arr[j+1] = key
        """

    st.subheader("🧾 Pseudocode")
    st.code(pseudo)

    st.subheader("⏱️ Complexity Table")
    st.table({
        "Case": ["Best Case", "Average Case", "Worst Case", "Space"],
        "Complexity": ["O(n)", "O(n²)", "O(n²)", "O(1)"]
    })

show_algorithm_info(algorithm)

st.subheader("📌 Initial Array")
draw_array(arr)

placeholder = st.empty()

def bubble_sort(arr):
    comparisons = 0
    swaps = 0
    n = len(arr)

    for i in range(n):
        for j in range(n - i - 1):
            comparisons += 1
            with placeholder.container():
                st.info(f"Comparing {arr[j]} and {arr[j+1]}")
                draw_array(arr, [j, j+1], list(range(n-i, n)))
                time.sleep(speed)

            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swaps += 1
                with placeholder.container():
                    st.warning("Swapping elements")
                    draw_array(arr, [j, j+1], list(range(n-i, n)))
                    time.sleep(speed)

    return arr, comparisons, swaps

def selection_sort(arr):
    comparisons = 0
    swaps = 0
    n = len(arr)

    for i in range(n):
        min_index = i

        for j in range(i + 1, n):
            comparisons += 1
            with placeholder.container():
                st.info(f"Comparing minimum {arr[min_index]} with {arr[j]}")
                draw_array(arr, [min_index, j], list(range(i)))
                time.sleep(speed)

            if arr[j] < arr[min_index]:
                min_index = j

        if min_index != i:
            arr[i], arr[min_index] = arr[min_index], arr[i]
            swaps += 1
            with placeholder.container():
                st.warning("Minimum element placed correctly")
                draw_array(arr, [i, min_index], list(range(i + 1)))
                time.sleep(speed)

    return arr, comparisons, swaps

def insertion_sort(arr):
    comparisons = 0
    shifts = 0
    n = len(arr)

    for i in range(1, n):
        key = arr[i]
        j = i - 1

        with placeholder.container():
            st.info(f"Selected key value: {key}")
            draw_array(arr, [i], list(range(i)))
            time.sleep(speed)

        while j >= 0:
            comparisons += 1

            if arr[j] > key:
                arr[j + 1] = arr[j]
                shifts += 1
                j -= 1

                with placeholder.container():
                    st.warning("Shifting element to right")
                    draw_array(arr, [j + 1], list(range(i)))
                    time.sleep(speed)
            else:
                break

        arr[j + 1] = key

    return arr, comparisons, shifts

if st.button("▶️ Start Simulation"):
    working_arr = arr.copy()

    if algorithm == "Bubble Sort":
        sorted_arr, comparisons, swaps = bubble_sort(working_arr)

    elif algorithm == "Selection Sort":
        sorted_arr, comparisons, swaps = selection_sort(working_arr)

    else:
        sorted_arr, comparisons, swaps = insertion_sort(working_arr)

    with placeholder.container():
        st.success("✅ Sorting Completed Successfully!")
        draw_array(sorted_arr, sorted_part=list(range(len(sorted_arr))))

    st.subheader("📊 Final Result")
    st.write("Sorted Output:", sorted_arr)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Comparisons", comparisons)
    col2.metric("Total Swaps / Shifts", swaps)
    col3.metric("Algorithm Used", algorithm)

    report = f"""
DAA Gaming Simulation Report

Algorithm Used: {algorithm}
Initial Array: {arr}
Sorted Output: {sorted_arr}
Total Comparisons: {comparisons}
Total Swaps/Shifts: {swaps}

This simulation explains sorting algorithms using gaming-style visualization.
Red bars show comparison, green bars show sorted elements.
"""

    st.download_button(
        label="📥 Download Report",
        data=report,
        file_name="sorting_simulation_report.txt",
        mime="text/plain"
    )
