import React from 'react';
import styled from 'styled-components';
import Form from './components/form';

function App() {
  return (
    <Wrapper>
      <h1>Wallet</h1>
      <p>Enter your username to show your user balance.</p>
      <Form/>
    </Wrapper>
  );
}

const Wrapper = styled.div`
  background-color:rgba(0,0,0,0.3);
  min-height:100vh;
  max-width:800px;
  margin: 0 auto;
`

export default App;
