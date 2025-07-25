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
  Link as MuiLink,
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
  TrendingUp,
  Shield,
  TrackChanges,
  Login as LoginIcon,
} from '@mui/icons-material';
import NextLink from 'next/link';
import { useRouter } from 'next/navigation';
import { Token } from '@/types'; // Importando o tipo Token

// Componente para os ícones de features
const FeatureIcon = ({ icon, text, color }: { icon: React.ReactNode; text: string; color: string }) => (
  <Stack alignItems="center" spacing={1}>
    <Box
      sx={{
        width: 40,
        height: 40,
        borderRadius: '12px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        bgcolor: `${color}.light`,
        color: `${color}.dark`,
      }}
    >
      {icon}
    </Box>
    <Typography variant="caption" color="text.secondary">
      {text}
    </Typography>
  </Stack>
);


export default function LoginPage() {
  const [username, setUsername] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [errors, setErrors] = React.useState({ username: '', password: '' });
  
  const [showPassword, setShowPassword] = React.useState(false);
  const [isLoading, setIsLoading] = React.useState(false);
  const [notification, setNotification] = React.useState({ open: false, message: '', severity: 'error' as 'error' | 'success' });
  const router = useRouter();

  // Estilos para sobrescrever o autopreenchimento do navegador que causa o fundo branco.
  const autofillFixStyles = {
    // Target the input element for autofill styles
    '& .MuiInputBase-input:-webkit-autofill': {
      // Usa um box-shadow interno para simular um background, enganando o navegador.
      WebkitBoxShadow: '0 0 0 100px #2d2d2d inset', // Cor de fundo escura que combina com o tema
      WebkitTextFillColor: '#fff', // Cor do texto para branco
      caretColor: '#fff', // Cor do cursor de digitação
      borderRadius: 'inherit', // Mantém o border-radius do input
    },
  };

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
    if (!validate()) {
      return;
    }

    setIsLoading(true);
    const data = { username, password };

    try {
      const response = await fetch('http://localhost:8000/api/auth/token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams(data),
      });

      // Tipando a resposta da API
      const result: Token | { detail: string } = await response.json();

      if (!response.ok) {
        throw new Error((result as { detail: string }).detail || 'Credenciais inválidas.');
      }

      localStorage.setItem('authToken', (result as Token).access_token);
      setNotification({ open: true, message: 'Login realizado com sucesso! Redirecionando...', severity: 'success' });
      
      setTimeout(() => {
        router.push('/');
      }, 1500);

    } catch (error: any) {
      console.error('Login error:', error);
      setNotification({ open: true, message: error.message || 'Ocorreu um erro. Tente novamente.', severity: 'error' });
    } finally {
      setIsLoading(false);
    }
  };

  const handleCloseNotification = () => {
    setNotification({ ...notification, open: false });
  };

  return (
    <>
      <Box
        sx={{
          position: 'fixed',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          zIndex: -1,
          background: (theme) => `linear-gradient(135deg, ${theme.palette.background.default} 0%, ${theme.palette.grey[900]} 50%, #000 100%)`,
        }}
      />
      <Container component="main" maxWidth="xs" sx={{ position: 'relative', zIndex: 1, py: 4 }}>
        <Stack alignItems="center" spacing={2} sx={{ mb: 4 }}>
          <Box
            sx={{
              width: 64,
              height: 64,
              bgcolor: 'primary.main',
              color: 'primary.contrastText',
              borderRadius: 4,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: 5,
            }}
          >
            <DirectionsCar sx={{ fontSize: 40 }} />
          </Box>
          <Typography component="h1" variant="h4" sx={{ fontWeight: 'bold', color: 'white' }}>
            Ride Finance
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            Seu controle financeiro na direção certa
          </Typography>
        </Stack>
        
        <Card
          sx={{
            p: 4,
            bgcolor: 'rgba(255, 255, 255, 0.05)',
            backdropFilter: 'blur(10px)',
            border: '1px solid rgba(255, 255, 255, 0.1)',
            boxShadow: '0 8px 32px 0 rgba(0, 0, 0, 0.37)',
          }}
        >
          <Typography variant="h5" component="h2" sx={{ mb: 1, fontWeight: 'medium', color: 'white' }}>
            Acessar sua conta
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
            Bem-vindo de volta!
          </Typography>
          
          <Box component="form" onSubmit={handleSubmit}>
            <Stack spacing={2}>
              <TextField
                label="Nome de Usuário"
                fullWidth
                autoFocus
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                error={!!errors.username}
                helperText={errors.username}
                sx={autofillFixStyles}
                FormHelperTextProps={{
                  sx: { color: 'white' },
                }}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <Email sx={{ color: 'white' }} />
                    </InputAdornment>
                  ),
                }}
              />
              <TextField
                label="Senha"
                type={showPassword ? 'text' : 'password'}
                fullWidth
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                error={!!errors.password}
                helperText={errors.password}
                sx={autofillFixStyles}
                FormHelperTextProps={{
                  sx: { color: 'white' },
                }}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <Lock sx={{ color: 'white' }} />
                    </InputAdornment>
                  ),
                  endAdornment: (
                    <InputAdornment position="end">
                      <IconButton onClick={() => setShowPassword(!showPassword)} edge="end" sx={{ color: 'white' }}>
                        {showPassword ? <VisibilityOff /> : <Visibility />}
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
            sx={{ fontWeight: 'bold' }}
          >
            Criar conta gratuita
          </Button>
        </Card>

        {/* Alterado de Grid para Stack (Flexbox) */}
        <Stack direction="row" spacing={4} justifyContent="center" sx={{ mt: 4 }}>
          <FeatureIcon icon={<TrendingUp />} text="Análises" color="success" />
          <FeatureIcon icon={<TrackChanges />} text="Metas" color="info" />
          <FeatureIcon icon={<Shield />} text="Seguro" color="secondary" />
        </Stack>

        <Typography variant="body2" color="text.secondary" align="center" sx={{ mt: 4 }}>
            © {new Date().getFullYear()} Ride Finance. Todos os direitos reservados.
        </Typography>
      </Container>
      
      <Snackbar
        open={notification.open}
        autoHideDuration={6000}
        onClose={handleCloseNotification}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert onClose={handleCloseNotification} severity={notification.severity} sx={{ width: '100%' }}>
          {notification.message}
        </Alert>
      </Snackbar>
    </>
  );
}
