import streamlit as st

# load file vocab


def load_vocab(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    words = sorted(set([line . strip() . lower() for line in lines]))
    return words


vocabs = load_vocab(file_path='./vocab.txt')

# define levenshtein distance calculation


def levenshtein_distance(source, target):
    # Tạo ma trận lưu trữ
    m, n = len(source), len(target)
    D = [[0] * (n + 1) for _ in range(m + 1)]

    # Khởi tạo hàng và cột đầu tiên
    for i in range(m + 1):
        D[i][0] = i
    for j in range(n + 1):
        D[0][j] = j

    # Tính toán các giá trị trong ma trận
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if source[i - 1] == target[j - 1]:
                cost = 0
            else:
                cost = 1
            D[i][j] = min(D[i - 1][j] + 1,    # Chi phí xoá
                          D[i][j - 1] + 1,    # Chi phí thêm
                          D[i - 1][j - 1] + cost)  # Chi phí thay thế

    # Giá trị tại ô cuối cùng là khoảng cách Levenshtein
    return D[m][n]


def main():
    st.title("Word Correction using Levenshtein Distance")
    word = st.text_input('Word:')

    if st.button("Compute"):

        # compute levenshtein distance
        leven_distances = dict()
        for vocab in vocabs:
            leven_distances[vocab] = levenshtein_distance(word, vocab)

        # sorted by distance
        sorted_distences = dict(
            sorted(leven_distances.items(), key=lambda item: item[1]))
        correct_word = list(sorted_distences.keys())[0]
        st.write('Correct word: ', correct_word)

        col1, col2 = st.columns(2)
        col1.write('Vocabulary:')
        col1.write(vocabs)

        col2.write('Distances:')
        col2.write(sorted_distences)


if __name__ == "__main__":
    main()
