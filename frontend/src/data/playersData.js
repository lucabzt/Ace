export const players = [
  {
    name: "Player 1",
    probWin: "75%",
    balance: 1000,
    bet: 50,
    folded: false,
    cards: [
      { rank: "ace", suit: "hearts", faceUp: true },
      { rank: "king", suit: "hearts", faceUp: true },
    ],
  },
  {
    name: "Bot 1",
    probWin: "40%",
    balance: 800,
    bet: 20,
    folded: false,
    cards: [
      { rank: "10", suit: "spades", faceUp: true },
      { rank: "jack", suit: "spades", faceUp: false },
    ],
  },
  {
    name: "Bot 2",
    probWin: "30%",
    balance: 1200,
    bet: 80,
    folded: true,
    cards: [
      { rank: "queen", suit: "diamonds", faceUp: true },
      { rank: "jack", suit: "diamonds", faceUp: true },
    ],
  },
  {
    name: "Player 2",
    probWin: "50%",
    balance: 600,
    bet: 30,
    folded: false,
    cards: [
      { rank: "queen", suit: "hearts", faceUp: true },
      { rank: "10", suit: "diamonds", faceUp: true },
    ],
  },
  {
    name: "Bot 3",
    probWin: "20%",
    balance: 1500,
    bet: 100,
    folded: false,
    cards: [
      { rank: "5", suit: "hearts", faceUp: true },
      { rank: "6", suit: "hearts", faceUp: false },
    ],
  },
  {
    name: "Player 3",
    probWin: "65%",
    balance: 900,
    bet: 70,
    folded: true,
    cards: [
      { rank: "7", suit: "diamonds", faceUp: false },
      { rank: "8", suit: "clubs", faceUp: true },
    ],
  },
  {
    name: "Player 4",
    probWin: "60%",
    balance: 1100,
    bet: 60,
    folded: false,
    cards: [
      { rank: "9", suit: "hearts", faceUp: true },
      { rank: "king", suit: "diamonds", faceUp: true },
    ],
  },
  {
    name: "Bot 4",
    probWin: "45%",
    balance: 950,
    bet: 50,
    folded: false,
    cards: [
      { rank: "jack", suit: "hearts", faceUp: true },
      { rank: "queen", suit: "clubs", faceUp: true },
    ],
  },
];
