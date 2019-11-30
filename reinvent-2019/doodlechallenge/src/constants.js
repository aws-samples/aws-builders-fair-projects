export const DOODLES = [
    { object: 'Glasses', similar: [] },
    { object: 'Bird', similar: [] },
    { object: 'Fish', similar: [] },
    { object: 'Flower', similar: [] },
    { object: 'Horse', similar: [] },
    { object: 'Shoes', similar: [] },
    { object: 'Airplane', similar: [] },
    { object: 'Scissors', similar: [] },
    { object: 'Car', similar: [] },
    { object: 'Bicycle', similar: [] },
    { object: 'Lightbulb', similar: [] },
    { object: 'Crab', similar: [] },

    { object: 'Fork', similar: [] },
    { object: 'Spider', similar: [] },
    { object: 'Teapot', similar: [] },
    
    { object: 'Sandals', similar: [] },
    { object: 'Mushroom', similar: [] },

    { object: 'Candle', similar: [] },
    { object: 'Headphones', similar: [] },
]

// Gets a random array of doodles to draw
export const getRandomDoodles = (amount) => {
    let a = DOODLES;
    for (let i = a.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]];
    }
    return a.slice(0,amount);
}

// Number rounds/doodles to draw per game
export const ROUNDS_PER_GAME = 5;
// Allow time to draw in seconds
export const DRAWTIME = 30;//20;
// List of available avatars to represent the players.
export const AVATARS = ['#FF0000', '#000FFF', '#FF00F3', '#00710E', '#66305C', 
'#FF5733', '#979A9A', '#B7950B', '#A3AF00'];
// Min players to play the game. This should be set to 2 or more
export const MIN_PLAYERS = 1;
// Maximum number of players. Technically you can have unlimited but the UI can only support so much before it becomes difficult to see.
export const MAX_PLAYERS = 6;
// Number of seconds to wait before starting the next round after all players have submitted their doodle.
export const NEXT_ROUND_DELAY = 5000;
// Number of seconds to wait while we show each doodle and the results of each doodle
export const NEXT_DOODLE_DELAY = 6000;