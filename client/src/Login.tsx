import { useState } from 'react';
import { Container } from 'react-bootstrap';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import useAuth from './hooks/useAuth';

function Login() {

  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const { onLogin } = useAuth();

  function handleSubmit(event: React.SyntheticEvent<HTMLFormElement>) {
    event.preventDefault()
    onLogin(email, password).then(() => {
      console.log("Logged in");
    }).catch((err: unknown) => {
      console.error(err);
    })
  }

  return (
    <Container className="p-3 my-5 w-25">
      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>Email address</Form.Label>
          <Form.Control onChange={e => { setEmail(e.target.value) }} type="email" placeholder="Enter email" />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicPassword">
          <Form.Label>Password</Form.Label>
          <Form.Control onChange={e => { setPassword(e.target.value) }} value={password} type="password" placeholder="Password" />
        </Form.Group>
        <Button variant="primary" type="submit">
          Login
        </Button>
      </Form>
    </Container>
  )
}

export default Login