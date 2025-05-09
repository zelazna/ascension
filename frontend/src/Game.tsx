import { Container } from 'react-bootstrap';
import useAuth from './hooks/useAuth';

function Game() {
  const { token } = useAuth();
  return (
    <Container className="p-3 my-5 w-25">
      <h2>GAME (Protected)</h2>
      <div>Authenticated as {token}</div>
    </Container>
  )
}

export default Game