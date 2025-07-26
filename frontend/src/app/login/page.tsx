'use client';

import * as React from 'react';
import {
  Container,
  Box,
  Typography,
  TextField,
  Button,
  Stack,
  InputAdornment,
  IconButton,
  Card,
  CircularProgress,
  Snackbar,
  Alert,
  Divider,
} from '@mui/material';
import {
  Visibility,
  VisibilityOff,
  Email,
  Lock,
  DirectionsCar,
  Login as LoginIcon,
} from '@mui/icons-material';
import NextLink from 'next/link';
import { useRouter } from 'next/navigation';
import { Token } from '@/types';

// A página agora não precisa de ThemeProvider ou CssBaseline, pois o layout já fornece.
export default function LoginPage() {
  const [username, setUsername] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [errors, setErrors] = React.useState({ username: '', password: '' });
  
  const [showPassword, setShowPassword] = React.useState(false);
  const [isLoading, setIsLoading] = React.useState(false);
  const [notification, setNotification] = React.useState({ open: false, message: '', severity: 'error' as 'error' | 'success' });
  const router = useRouter();

  const validate = () => {
    const tempErrors = { username: '', password: '' };
    let isValid = true;
    if (!username) {
      isValid = false;
      tempErrors.username = 'O nome de usuário é obrigatório.';
    }
    if (!password) {
        isValid = false;
        tempErrors.password = 'A senha é obrigatória.';
    }
    setErrors(tempErrors);
    return isValid;
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!validate()) return;
    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/auth/token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ username, password }),
      });
      const result: Token | { detail: string } = await response.json();
      if (!response.ok) throw new Error((result as { detail: string }).detail || 'Credenciais inválidas.');
      localStorage.setItem('authToken', (result as Token).access_token);
      setNotification({ open: true, message: 'Login realizado com sucesso!', severity: 'success' });
      setTimeout(() => router.push('/'), 1500);
    } catch (error: any) {
      setNotification({ open: true, message: error.message || 'Ocorreu um erro.', severity: 'error' });
    } finally {
      setIsLoading(false);
    }
  };

  const handleCloseNotification = () => {
    setNotification({ ...notification, open: false });
  };

  return (
    <Container component="main" maxWidth="xs" sx={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', height: '100vh' }}>
      <Stack alignItems="center" spacing={2} sx={{ mb: 4 }}>
        <Box
          sx={{
            width: 60,
            height: 60,
            bgcolor: 'primary.main',
            color: 'primary.contrastText',
            borderRadius: 4,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0px 8px 20px rgba(0, 118, 255, 0.3)',
          }}
        >
          <DirectionsCar sx={{ fontSize: 36 }} />
        </Box>
        <Typography component="h1" variant="h4" sx={{ fontWeight: 'bold' }}>
          Ride Finance
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Seu controle na direção certa
        </Typography>
      </Stack>
      
      <Card
        elevation={0}
        sx={{
          p: 4,
          bgcolor: 'rgba(255, 255, 255, 0.03)',
          border: '1px solid rgba(255, 255, 255, 0.1)',
        }}
      >
        <Typography variant="h5" component="h2" sx={{ mb: 3, fontWeight: 'medium', textAlign: 'center' }}>
          Acessar sua conta
        </Typography>
        
        <Box component="form" onSubmit={handleSubmit}>
          <Stack spacing={2.5}>
            <TextField
              label="Nome de Usuário"
              fullWidth
              autoComplete="username"
              autoFocus
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              error={!!errors.username}
              helperText={errors.username}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <Email sx={{ color: 'text.secondary' }} />
                  </InputAdornment>
                ),
              }}
            />
            <TextField
              label="Senha"
              type={showPassword ? 'text' : 'password'}
              fullWidth
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              error={!!errors.password}
              helperText={errors.password}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <Lock sx={{ color: 'text.secondary' }} />
                  </InputAdornment>
                ),
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton onClick={() => setShowPassword(!showPassword)} edge="end">
                      {showPassword ? <VisibilityOff sx={{ color: 'text.secondary' }} /> : <Visibility sx={{ color: 'text.secondary' }} />}
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              size="large"
              disabled={isLoading}
              startIcon={isLoading ? <CircularProgress size={20} color="inherit" /> : <LoginIcon />}
              sx={{ mt: 2, py: 1.5, fontWeight: 'bold' }}
            >
              {isLoading ? 'Entrando...' : 'Entrar'}
            </Button>
          </Stack>
        </Box>
        
        <Divider sx={{ my: 3, color: 'text.secondary', fontSize: '0.8rem' }}>ou</Divider>
        
        <Button
          component={NextLink}
          href="/register"
          fullWidth
          variant="outlined"
          size="large"
        >
          Criar conta gratuita
        </Button>
      </Card>
    </Container>
  );
}
