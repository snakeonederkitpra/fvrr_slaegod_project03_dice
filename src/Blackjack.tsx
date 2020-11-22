import React, { useState, useEffect } from 'react';
import {
  Button, Paper, makeStyles, Typography, Input, Box,
} from '@material-ui/core';
import BlackjackGame from './BlackjackGame';

const useStyles = makeStyles(() => ({
  root: {
    flexGrow: 1,
    top: '40px',
    backgroundColor: '#136207',
    height: '80vh',
    width: '96%',
    textAlign: 'center',
    margin: 'auto',
    padding: '20px',
  },
}));

const rules = (
  <Box style={{ margin: 'auto', width: '35%' }}>
    <Typography variant="h6">Rules:</Typography>
    <Box style={{ textAlign: 'left', paddingLeft: '40px' }}>
      <p>1. Goal of blackjack is to beat the dealer&apos;s hand without going over 21</p>
      <p>2. Jack, Queen and King are worth 10 points</p>
      <p>3. Aces are worth 1 or 11 points. Which ever makes the hand better</p>
      <p>4. Value cards are worth its repective value</p>
      <p>7. &apos;Hit&apos; is to ask for another card.</p>
      <p>8. &apos;Stand&apos; is to keep your total and end asking for cards</p>
      <p>11. Dealer must hit until total is above 17</p>
      <p>12. Reward is worth double of your bet</p>
    </Box>
  </Box>
);

function Blackjack() {
  const [message, setMessage] = useState<String>('');
  const [errorMessage, setErrorMessage] = useState<String>('');
  const [gameState, setGameState] = useState<number>(0);
  const [pool, setPool] = useState<string>('500');
  function HandlePool(event) {
    const { value: NewValue } = event.target;
    setPool(NewValue);
  }
  function PlayBlackJack() {
    const num = Number(pool);
    if (/^\d*$/.test(pool) === false || Number.isNaN(num)) {
      setErrorMessage('Invalid Input');
    } else if (num < 500) {
      setPool('500');
      setErrorMessage('Minimum pool required is 500 tickets');
    } else {
      fetch('/api/blackjack/checkfunds', {
        method: 'POST',
        body: JSON.stringify({
          amount: Number(pool),
        }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.success) {
            setGameState(2);
          } else {
            setErrorMessage(data.message);
          }
        });
    }
  }
  useEffect(() => {
    fetch('/api/blackjack/play')
      .then((res) => res.json())
      .then((data) => {
        if (data.success === true) {
          setMessage(data.message);
          setGameState(1);
        } else {
          setErrorMessage(data.message);
        }
      });
  }, []);
  const classes = useStyles();
  return (
    <div className="blackjack-page">
      <Paper className={classes.root} style={{ position: 'relative', top: '20px' }}>
        {(() => {
          switch (gameState) {
            case 1: return (
              <div className="wagering-box">
                <Typography variant="h4" style={{ marginBottom: '15px' }}>{message}</Typography>
                {rules}
                <Input type="text" defaultValue={pool} onChange={HandlePool} />
                <Button variant="contained" type="button" onClick={PlayBlackJack} className="blackjack-play">Play</Button>
                <Typography variant="h6">{errorMessage}</Typography>
              </div>
            );
            case 2: return (
              <BlackjackGame pool={pool} />
            );
            default: return (
              <div className="blackjack-error">
                {rules}
                <Typography variant="h6">{errorMessage}</Typography>
              </div>
            );
          }
        })()}
      </Paper>
    </div>
  );
}

export default Blackjack;