import streamlit as st
import streamlit.components.v1 as components
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import random
import time
import html

st.set_page_config(page_title="DAA Sorting Game", layout="wide")

st.title("🎮 DAA Sorting Visualizer with Teacher Audio")
st.write("Fast sorting animation with teacher voice explanation, quiz, progress, and report")

st.sidebar.header("⚙️ Controls")

algorithm = st.sidebar.selectbox(
    "Choose Algorithm",
    ["Bubble Sort", "Selection Sort", "Insertion Sort"]
)

learning_mode = st.sidebar.selectbox(
    "Learning Mode",
    ["Teacher Mode", "Student Mode"]
)

input_type = st.sidebar.radio("Input Type", ["Random Array", "Custom Array"])
size = st.sidebar.slider("Array Size", 4, 12, 6)

# FAST ANIMATION SETTINGS
speed = st.sidebar.slider("Animation Delay", 0.1, 2.0, 0.5)
voice_rate = st.sidebar.slider("Voice Speed", 0.4, 1.2, 0.75)

audio_enabled = st.sidebar.checkbox("🔊 Enable Voice Explanation", value=True)

voice_gender = st.sidebar.selectbox(
    "🎤 Voice Type",
    ["Female", "Male"]
)

if input_type == "Custom Array":
    custom_input = st.sidebar.text_input(
        "Enter numbers separated by comma",
        "45, 12, 78, 23, 56"
    )
    try:
        arr = [int(x.strip()) for x in custom_input.split(",")]
    except:
        st.error("Enter valid numbers like: 10, 20, 30")
        st.stop()
else:
    if "array" not in st.session_state or len(st.session_state.array) != size:
        st.session_state.array = [random.randint(10, 100) for _ in range(size)]

    if st.sidebar.button("🔄 Generate New Array"):
        st.session_state.array = [random.randint(10, 100) for _ in range(size)]

    arr = st.session_state.array.copy()

def speak(text):
    if audio_enabled:
        safe_text = html.escape(text).replace("\n", " ")

        if voice_gender == "Female":
            gender_script = """
            selectedVoice = voices.find(v =>
                v.name.toLowerCase().includes('female') ||
                v.name.toLowerCase().includes('zira') ||
                v.name.toLowerCase().includes('samantha') ||
                v.name.toLowerCase().includes('google uk english female') ||
                v.name.toLowerCase().includes('google us english')
            );
            """
        else:
            gender_script = """
            selectedVoice = voices.find(v =>
                v.name.toLowerCase().includes('male') ||
                v.name.toLowerCase().includes('david') ||
                v.name.toLowerCase().includes('mark') ||
                v.name.toLowerCase().includes('google uk english male') ||
                v.name.toLowerCase().includes('google us english')
            );
            """

        components.html(
            f"""
            <script>
            function runSpeech() {{

                let text = `{safe_text}`;
                let speech = new SpeechSynthesisUtterance(text);

                speech.lang = "en-US";
                speech.rate = {voice_rate};
                speech.pitch = 1;
                speech.volume = 1;

                let voices = window.speechSynthesis.getVoices();
                let selectedVoice = null;

                {gender_script}

                if (selectedVoice) {{
                    speech.voice = selectedVoice;
                }}

                window.speechSynthesis.cancel();

                setTimeout(() => {{
                    window.speechSynthesis.speak(speech);
                }}, 200);
            }}

            if (window.speechSynthesis.getVoices().length === 0) {{
                window.speechSynthesis.onvoiceschanged = runSpeech;
            }} else {{
                runSpeech();
            }}
            </script>
            """,
            height=0
        )

        # FAST voice waiting time
        estimated_time = max(1.0, len(text.split()) * 0.22)
        time.sleep(estimated_time)

def mode_text(long_text, short_text):
    return long_text if learning_mode == "Teacher Mode" else short_text

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
    ax.set_xlabel("Array Position")
    ax.set_ylabel("Value")

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

st.markdown("""
### 🎨 Color Legend
🟥 Red = Comparing elements  
🟩 Green = Sorted part  
🟦 Blue = Unsorted part  
""")

def show_info(algo):
    st.subheader("📘 Algorithm Explanation")

    if algo == "Bubble Sort":
        st.write("""
        Bubble Sort compares adjacent elements.
        If the left value is greater than the right value, it swaps them.
        After each pass, the largest element moves to its correct position.
        """)
        pseudo = """
for i = 0 to n-1:
    for j = 0 to n-i-2:
        if arr[j] > arr[j+1]:
            swap arr[j], arr[j+1]
        """

    elif algo == "Selection Sort":
        st.write("""
        Selection Sort finds the smallest value from the unsorted part.
        Then it places that smallest value in the correct position.
        """)
        pseudo = """
for i = 0 to n-1:
    min_index = i
    for j = i+1 to n:
        if arr[j] < arr[min_index]:
            min_index = j
    swap arr[i], arr[min_index]
        """

    else:
        st.write("""
        Insertion Sort selects one key value.
        It shifts larger values to the right and inserts the key in the correct place.
        """)
        pseudo = """
for i = 1 to n-1:
    key = arr[i]
    while previous values > key:
        shift values right
    insert key
        """

    st.subheader("🧾 Pseudocode")
    st.code(pseudo)

    st.subheader("⏱️ Complexity Table")
    st.table({
        "Case": ["Best Case", "Average Case", "Worst Case", "Space Complexity"],
        "Complexity": ["O(n)", "O(n²)", "O(n²)", "O(1)"]
    })

show_info(algorithm)

st.subheader("📌 Initial Array")
draw_array(arr)

progress_bar = st.progress(0)
placeholder = st.empty()
status_box = st.empty()
array_box = st.empty()
metric_box = st.empty()

def show_metrics(comparisons, swaps, current_step):
    with metric_box.container():
        c1, c2, c3 = st.columns(3)
        c1.metric("Current Step", current_step)
        c2.metric("Comparisons", comparisons)
        c3.metric("Swaps / Shifts", swaps)

def show_array(arr):
    array_box.code(f"Current Array: {arr}")

def bubble_sort(arr):
    comparisons = 0
    swaps = 0
    n = len(arr)
    total_steps = max(1, n * (n - 1) // 2)
    step = 0

    intro = mode_text(
        "Welcome students. Now we are learning Bubble Sort step by step. "
        "Bubble Sort compares two adjacent values. If the left value is greater than the right value, we swap them. "
        "After each pass, the largest unsorted element reaches the correct position.",
        "Bubble Sort compares adjacent values and swaps them if they are in wrong order."
    )
    status_box.info(intro)
    speak(intro)
    time.sleep(speed)

    for i in range(n - 1):
        pass_intro = mode_text(
            f"Pass {i + 1} is starting. In this pass, the largest value from the unsorted part will move towards the right side.",
            f"Pass {i + 1} started."
        )
        status_box.info(pass_intro)
        speak(pass_intro)
        time.sleep(speed)

        for j in range(n - i - 1):
            comparisons += 1
            step += 1
            progress_bar.progress(min(step / total_steps, 1.0))
            show_metrics(comparisons, swaps, step)
            show_array(arr)

            left = arr[j]
            right = arr[j + 1]

            compare_text = mode_text(
                f"Now we compare {left} and {right}. {left} is on the left side and {right} is on the right side. "
                f"Our rule is simple. If left value is greater than right value, then swap them.",
                f"Comparing {left} and {right}."
            )

            with placeholder.container():
                st.info(compare_text)
                draw_array(arr, [j, j + 1], list(range(n - i, n)))

            speak(compare_text)
            time.sleep(speed)

            if left > right:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1

                swap_text = mode_text(
                    f"{left} is greater than {right}. So the order is wrong. "
                    f"We swap them. After swapping, {right} moves left and {left} moves right.",
                    f"{left} is greater than {right}. Swap needed."
                )

                with placeholder.container():
                    st.error(f"Wrong Order Detected: {left} > {right}")
                    st.warning(swap_text)
                    draw_array(arr, [j, j + 1], list(range(n - i, n)))

                speak(swap_text)
                time.sleep(speed)

            else:
                no_swap_text = mode_text(
                    f"{left} is not greater than {right}. So both values are already in correct order. No swap is required.",
                    f"{left} and {right} are already correct. No swap."
                )

                with placeholder.container():
                    st.success(f"Correct Order: {left} ≤ {right}")
                    st.success(no_swap_text)
                    draw_array(arr, [j, j + 1], list(range(n - i, n)))

                speak(no_swap_text)
                time.sleep(speed)

        fixed = arr[n - i - 1]
        end_pass = mode_text(
            f"Pass {i + 1} completed. The value {fixed} is now fixed in its correct sorted position.",
            f"Pass {i + 1} completed. {fixed} is fixed."
        )
        status_box.success(end_pass)
        speak(end_pass)
        time.sleep(speed)

    final_text = "Bubble Sort completed. The array is sorted from smallest to largest."
    speak(final_text)
    return arr, comparisons, swaps

def selection_sort(arr):
    comparisons = 0
    swaps = 0
    n = len(arr)
    total_steps = max(1, n * (n - 1) // 2)
    step = 0

    intro = mode_text(
        "Welcome students. Now we are learning Selection Sort. "
        "Selection Sort finds the smallest value from the unsorted part and places it in the correct position.",
        "Selection Sort finds the smallest value and places it correctly."
    )
    status_box.info(intro)
    speak(intro)
    time.sleep(speed)

    for i in range(n):
        min_index = i

        start_text = mode_text(
            f"Now position {i + 1} is considered. We assume {arr[min_index]} is the current minimum value.",
            f"Position {i + 1}: current minimum is {arr[min_index]}."
        )
        status_box.info(start_text)
        speak(start_text)
        time.sleep(speed)

        for j in range(i + 1, n):
            comparisons += 1
            step += 1
            progress_bar.progress(min(step / total_steps, 1.0))
            show_metrics(comparisons, swaps, step)
            show_array(arr)

            current_min = arr[min_index]
            current_value = arr[j]

            explanation = mode_text(
                f"We compare current minimum {current_min} with {current_value}. "
                f"If {current_value} is smaller, it becomes the new minimum.",
                f"Comparing {current_min} and {current_value}."
            )

            with placeholder.container():
                st.info(explanation)
                draw_array(arr, [min_index, j], list(range(i)))

            speak(explanation)
            time.sleep(speed)

            if arr[j] < arr[min_index]:
                min_index = j
                new_min_text = mode_text(
                    f"New minimum found. The new minimum value is {arr[min_index]}.",
                    f"New minimum is {arr[min_index]}."
                )
                status_box.success(new_min_text)
                speak(new_min_text)
                time.sleep(speed)

        if min_index != i:
            old = arr[i]
            minimum = arr[min_index]
            arr[i], arr[min_index] = arr[min_index], arr[i]
            swaps += 1

            swap_text = mode_text(
                f"The smallest value is {minimum}. We swap {old} with {minimum}. Now {minimum} is fixed.",
                f"Swap {old} and {minimum}."
            )

            with placeholder.container():
                st.warning(swap_text)
                draw_array(arr, [i, min_index], list(range(i + 1)))

            speak(swap_text)
            time.sleep(speed)

    final_text = "Selection Sort completed. The array is sorted from smallest to largest."
    speak(final_text)
    return arr, comparisons, swaps

def insertion_sort(arr):
    comparisons = 0
    shifts = 0
    n = len(arr)
    total_steps = max(1, n * (n - 1) // 2)
    step = 0

    intro = mode_text(
        "Welcome students. Now we are learning Insertion Sort. "
        "Insertion Sort takes one key value and inserts it into the correct position in the sorted part.",
        "Insertion Sort places each key value in its correct position."
    )
    status_box.info(intro)
    speak(intro)
    time.sleep(speed)

    for i in range(1, n):
        key = arr[i]
        j = i - 1

        key_text = mode_text(
            f"The selected key value is {key}. We compare this key with previous sorted values from right to left.",
            f"Selected key is {key}."
        )

        with placeholder.container():
            st.info(key_text)
            draw_array(arr, [i], list(range(i)))

        speak(key_text)
        time.sleep(speed)

        while j >= 0 and arr[j] > key:
            comparisons += 1
            step += 1
            progress_bar.progress(min(step / total_steps, 1.0))
            show_metrics(comparisons, shifts, step)
            show_array(arr)

            move = arr[j]
            arr[j + 1] = arr[j]
            shifts += 1

            shift_text = mode_text(
                f"{move} is greater than key value {key}. So {move} shifts one position to the right.",
                f"{move} shifts right."
            )

            with placeholder.container():
                st.warning(shift_text)
                draw_array(arr, [j, j + 1], list(range(i)))

            speak(shift_text)
            time.sleep(speed)
            j -= 1

        arr[j + 1] = key

        insert_text = mode_text(
            f"Now key value {key} is inserted into its correct position. The left side is sorted up to this point.",
            f"Key {key} inserted correctly."
        )

        with placeholder.container():
            st.success(insert_text)
            draw_array(arr, [j + 1], list(range(i + 1)))

        speak(insert_text)
        time.sleep(speed)

    final_text = "Insertion Sort completed. The array is sorted from smallest to largest."
    speak(final_text)
    return arr, comparisons, shifts

if st.button("▶️ Start Simulation"):
    working_arr = arr.copy()

    if algorithm == "Bubble Sort":
        sorted_arr, comparisons, swaps = bubble_sort(working_arr)
    elif algorithm == "Selection Sort":
        sorted_arr, comparisons, swaps = selection_sort(working_arr)
    else:
        sorted_arr, comparisons, swaps = insertion_sort(working_arr)

    progress_bar.progress(1.0)

    with placeholder.container():
        st.success("✅ Sorting Completed Successfully!")
        draw_array(sorted_arr, sorted_part=list(range(len(sorted_arr))))

    final_summary = (
        f"Sorting completed successfully. "
        f"The algorithm used is {algorithm}. "
        f"Total comparisons are {comparisons}. "
        f"Total swaps or shifts are {swaps}. "
        f"The final sorted array is {sorted_arr}."
    )
    status_box.success(final_summary)
    speak(final_summary)

    st.subheader("📊 Final Result")
    st.write("Initial Array:", arr)
    st.write("Sorted Output:", sorted_arr)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Comparisons", comparisons)
    col2.metric("Total Swaps / Shifts", swaps)
    col3.metric("Algorithm Used", algorithm)

    st.subheader("🧠 Quick Quiz")
    answer = st.radio(
        "In sorting, what should we do if the left element is greater than the right element?",
        ["Swap the elements", "Delete the elements", "Ignore the elements"]
    )

    if st.button("Check Answer"):
        if answer == "Swap the elements":
            st.success("Correct! We swap the elements to arrange them in ascending order.")
        else:
            st.error("Wrong. Correct answer is: Swap the elements.")

    report = f"""
DAA Sorting Simulation Report

Algorithm Used: {algorithm}
Learning Mode: {learning_mode}
Voice Type: {voice_gender}

Initial Array: {arr}
Sorted Output: {sorted_arr}

Total Comparisons: {comparisons}
Total Swaps/Shifts: {swaps}

Color Legend:
Red = Comparing Elements
Green = Sorted Elements
Blue = Unsorted Elements

This simulation explains sorting step by step with visual animation, progress tracking, and teacher-style audio narration.
"""

    st.download_button(
        label="📥 Download Report",
        data=report,
        file_name="sorting_simulation_report.txt",
        mime="text/plain"
    )
