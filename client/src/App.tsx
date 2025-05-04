import { Button, Container, Nav, Navbar } from 'react-bootstrap';
import { Navigate, NavLink, Outlet, Route, Routes, useLocation } from 'react-router';
import Game from './Game';
import Home from './Home';
import Login from './Login';
import './App.css';
import NotFound from './NotFound';
import useAuth from './hooks/useAuth';
import AuthProvider from './auth/AuthProvider';


interface ProtectedRouteProps {
  children: React.ReactNode;
}

const ProtectedRoute = ({ children }: ProtectedRouteProps) => {
  const { token } = useAuth();
  const location = useLocation();

  if (!token) {
    return <Navigate to="/login" replace state={{ from: location }} />;
  }

  return children;
};

const Navigation = () => {
  const location = useLocation();
  const { token, onLogout } = useAuth();

  return (
    <Navbar expand="lg" className="bg-body-tertiary">
      <Container>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav activeKey={location.pathname} className="me-auto">
            <Nav.Link as={NavLink} to="/">Home</Nav.Link>
            <Nav.Link as={NavLink} to="/game">Game</Nav.Link>
          </Nav>
          <Nav className="ms-auto">
            {token && (
              <Button
                className="ms-auto"
                type="button"
                onClick={() => {
                  onLogout().catch((error: unknown) => {
                    console.error('Logout failed:', error);
                  });
                }}
              >
                Sign Out
              </Button>
            )}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

const Layout = () => {
  return (<>
    <Navigation />
    <main style={{ padding: '1rem 0' }}><Outlet /></main>
  </>)
};


function App() {
  return (
    <>
      <AuthProvider>
        <Routes>
          <Route element={<Layout />}>
            <Route index element={<Home />} />
            <Route path="home" element={<Home />} />
            <Route path="login" element={<Login />} />
            <Route
              path="game"
              element={
                <ProtectedRoute>
                  <Game />
                </ProtectedRoute>
              }
            />
            <Route path="*" element={<NotFound />} />
          </Route>
        </Routes>
      </AuthProvider>
    </>
  )
}

export default App
