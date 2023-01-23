from open_ai import Dalle2

def main():
    dalle2 = Dalle2()
    url = dalle2.create(description="An unicorn running through the clouds", url_mode=True)
    print(f'url: {url}')

if __name__ == '__main__':
    main()