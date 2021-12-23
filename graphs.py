from matplotlib import pyplot


def pieGraph(total, nombres, cantidades):
    disponible = total
    for can in cantidades:
        disponible -= can
    cantidades.append(disponible)
    nombres.append("Stock disponible")

    fig1, ax1 = pyplot.subplots()
    ax1.pie(cantidades, labels=nombres, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')

    pyplot.show()




