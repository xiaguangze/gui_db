def get_table_name(sql):
    lists = sql.split(" ")
    table_name = lists[lists.index("from") + 1]

    return table_name


def get_table_pages(table_count, page_size):
    number = table_count % page_size
    if number:
        max_page = int(table_count/page_size) + 1
    else:
        max_page = int(table_count/page_size)

    return max_page


def show_pages(max_page, current_page):
    show_list = []
    if max_page > 6 and max_page > current_page + 3:
        if current_page == 1:
            show_list = [1, 2, 3, -1, max_page]
        elif current_page == 2:
            show_list = [1, 2, 3, 4, -1, max_page]
        elif current_page == 3:
            show_list = [1, 2, 3, 4, 5, -1, max_page]
        else:
            show_list = [1, -1, current_page-2, current_page-1, current_page, current_page+1, current_page+2, -1, max_page]
    elif max_page > 6 and current_page < max_page <= current_page + 3:
        show_list = [1, -1, current_page - 2, current_page - 1, current_page]
        for num in range(current_page+1, max_page+1):
            show_list.append(num)
    elif current_page == max_page > 6:
        show_list = [1, -1, current_page-2, current_page-1, current_page]
    elif max_page <= 6:
        for num in range(1, max_page+1):
            show_list.append(num)

    return show_list
