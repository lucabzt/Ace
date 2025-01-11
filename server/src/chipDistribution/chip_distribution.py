
class ChipDistributor:
    def __init__(self):
        self.G = 1000
        self.chip_count = [150, 50, 25, 50, 50, 25]
        self.chip_value = [5, 10, 25, 100, 500, 1000]
        self.chip_type_count = 6
        self.gesW = 0
        for i in range(self.chip_type_count):
            self.gesW += self.chip_count[i] * self.chip_value[i]

        self.max_players = self.gesW // self.G
        self.spielerChipVerteilung = self.recursion()

        if self.spielerChipVerteilung is None:
            print("Keine \"schöne\" Lösung gefunden")

        for i in range(self.chip_type_count):
            print(self.spielerChipVerteilung[i] + " Chips mit Wert " + self.chip_value[i])

        print("\nBei max. " + str(self.max_players) + " Spielern")

    def recursion(self):
        if self.max_players == 0:
            if self.chip_type_count == 0:
                return None
            self.chip_type_count -= 1
            self.max_players = self.gesW // self.G

        spielerChipVerteilung = [] * self.chip_type_count
        for i in range(self.chip_type_count):
            spielerChipVerteilung[i] = self.chip_count[i] / self.max_players

        spielerWert = 0

        for i in range(self.chip_type_count):
            spielerWert += spielerChipVerteilung[i] * self.chip_value[i]

        if spielerWert == self.G:
            return spielerChipVerteilung
        elif spielerWert < self.G:
            self.max_players -= 1
            return self.recursion()
        else:
            abgebbareChips = [0] * self.chip_value.__len__()

            for i in range(self.spielerChipVerteilung):
                abgebbareChips[i] = max(spielerChipVerteilung[i] - 1, 0)

            abzuziehendeChips = self.minCoinsWithDistribution(self.chip_value, abgebbareChips, spielerWert - self.G)
            if abzuziehendeChips is None:
                self.max_players -= 1
                return self.recursion()

            for i in range(self.chip_type_count):
                spielerChipVerteilung[i] -= abzuziehendeChips[i]
                if spielerChipVerteilung[i] < 0:
                    print("WTF ChatGPT (1)")

            spielerWert = 0
            for i in range(self.chip_type_count):
                spielerWert += spielerChipVerteilung[i] * self.chip_value[i]

            if spielerWert != self.G:
                print("WTF ChatGPT (2)")

            return spielerChipVerteilung

    def minCoinsWithDistribution(self, coins, maxCounts, target):
        dp = [0] * (target + 1)
        for i in range(len(dp)):
            dp[i] = 99999999
        dp[0] = 0

        used_coins = [[0] * coins.__len__() for _ in range(target + 1)]

        for i in range(coins.__len__()):
            coin = coins[i]
            maxCount = maxCounts[i]

            for j in range(target, -1, -1):
                for k in range(1, maxCount + 1):
                    if k * coin <= j:
                        if dp[j - k * coin] != float('inf'):
                            new_count = dp[j - k * coin] + k
                            if new_count < dp[j]:
                                dp[j] = new_count

                                # Aktualisiere die Münzverteilung
                                used_coins[j] = used_coins[j - k * coin][:]  # Copy the distribution
                                used_coins[j][i] += k

        if dp[target] == 99999999:
            return None

        return used_coins[target]


def main():
    distributor = ChipDistributor()


if __name__ == "__main__":
    main()
