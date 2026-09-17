from src.data.market_data import get_market_data


def main():

    df = get_market_data(
        ticker="^GSPC",
        start="2026-01-01",
        end="2026-09-18",
    )

    print("\n=== MARKET DATA ===\n")

    print(df.head())

    print("\nShape:")
    print(df.shape)

    print("\nLatest observations:")
    print(df.tail())


if __name__ == "__main__":
    main()
