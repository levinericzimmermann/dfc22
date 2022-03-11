import dfc22

print(dfc22.constants.NON_TERMINAL_PAIR_TO_PAGE_TUPLE)

print("")

for (
    non_terminal_pair,
    page_tuple,
) in dfc22.constants.NON_TERMINAL_PAIR_TO_PAGE_TUPLE.items():
    print(non_terminal_pair)
    print([page.duration for page in page_tuple])
    print([len(page) for page in page_tuple])
    for page in page_tuple:
        print(
            "NEW PAGE. It has: {} paragraphs, {} sentences, {} words.".format(
                len(page),
                sum(len(para) for para in page),
                sum(sum(len(sen) for sen in para) for para in page),
            )
        )
        print('')
        print(page.as_xsampa_text)
        print('')
    print("")

print(len(dfc22.constants.NON_TERMINAL_PAIR_TO_PAGE_TUPLE))
