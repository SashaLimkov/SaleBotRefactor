def get_paginator_context(page: int, num_pages: int) -> dict:
    """Возвращает контекст для рендера пагинатора"""
    if page >= 2:
        page_range = [i for i in range(page - 1, page + 2) if i <= num_pages]
    else:
        page_range = [i for i in range(1, 4) if i <= num_pages]
    context = {
        'page': page,
        'page_range': page_range,
        'page_last': max(page_range),
        'page_max': num_pages,
        'next': max(page_range) + 1,
        'last': page - 2
    }
    return context
