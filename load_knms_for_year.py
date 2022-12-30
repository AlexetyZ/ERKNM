from ERKNM_http import Erknm


def main():
    year = int(input('Enter the year, to reload datas knm (format: "YYYY")'))
    Erknm().get_all_knm_for_a_year(year=year)


if __name__ == '__main__':
    main()
