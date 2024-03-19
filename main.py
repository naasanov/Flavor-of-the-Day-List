from flavor import Flavor

def main():
    f = Flavor("","",[""])
    
    for i in range(100):
        try:
            FODList = f.makeFODList(30)
            for item, j in zip(FODList, range(1,len(FODList)+1)):
                print(f"{j}: {item.name}, {item.base}, {item.toppings}")
            break
        except:
            continue

if __name__ == '__main__':
    main()