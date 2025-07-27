// srclauss/ride_finance/ride_finance-c3c4ede5d333e8498b4716c91b9fe5367546ca13/frontend/src/app/register/page.tsx
'use client';

import * as React from 'react';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Link from '@mui/material/Link';
import Box from '@mui/material/Box';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import InputAdornment from '@mui/material/InputAdornment';
import IconButton from '@mui/material/IconButton';
import { Visibility, VisibilityOff, PersonOutline, EmailOutlined, PhoneOutlined, AccountCircleOutlined } from '@mui/icons-material';
import ThemeRegistry from '@/components/ThemeRegistry';

export default function SignUp() {
    const [fullName, setFullName] = useState('');
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [phone, setPhone] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const [error, setError] = useState('');
    const router = useRouter();

    const handleClickShowPassword = () => setShowPassword((show) => !show);
    const handleMouseDownPassword = (event: React.MouseEvent<HTMLButtonElement>) => {
        event.preventDefault();
    };
    const onBlurTelefone = (event: React.FocusEvent<HTMLInputElement>) => {
        // Formata o número de telefone ao perder o foco
        let value = event.target.value.replace(/\D/g, ''); // Remove tudo que não é dígito
        if (value.length === 11) {
            value = value.replace(/^(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
        } else if (value.length === 10) {
            value = value.replace(/^(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
        }
        // Atualiza o estado apenas com o valor formatado
        setPhone(value);
    }
    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        setError('');

        if (password !== confirmPassword) {
            setError('As senhas não coincidem.');
            return;
        }

        if (password.length < 6) {
            setError('A senha deve ter no mínimo 6 caracteres.');
            return;
        }

        try {
            const response = await fetch('http://localhost:8000/api/auth/register/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: email,
                    full_name: fullName,
                    username: username,
                    password: password,
                    phone: phone.replace(/\D/g, '') // Envia apenas os números para o backend
                }),
            });

            const data = await response.json();

            if (response.ok) {
                // Registro bem-sucedido, redireciona para a página de pagamento
                router.push('/payment');
            } else {
                // Falha no registro
                if (data.detail) {
                    if (Array.isArray(data.detail)) {
                        // Lida com erros de validação do FastAPI (HTTP 422)
                        const firstError = data.detail[0];
                        setError(`Erro no campo '${firstError.loc[1]}': ${firstError.msg}`);
                    } else {
                        // Lida com outros erros baseados em string (ex: HTTP 400)
                        setError(data.detail);
                    }
                } else {
                    setError('Ocorreu um erro durante o registro. Status: ' + response.status);
                }
            }
        } catch (err) {
            setError('Não foi possível conectar ao servidor. Tente novamente mais tarde.');
        }
    };

    return (
        <ThemeRegistry>
            <Container component="main" maxWidth="xs">
                <CssBaseline />
                <Box
                    sx={{
                        marginTop: 8,
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                    }}
                >
                    <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
                        <LockOutlinedIcon />
                    </Avatar>
                    <Typography component="h1" variant="h5">
                        Criar Conta
                    </Typography>
                    <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            id="fullName"
                            label="Nome Completo"
                            name="fullName"
                            autoComplete="name"
                            autoFocus
                            value={fullName}
                            onChange={(e) => setFullName(e.target.value)}
                            slotProps={
                                {
                                    input: {
                                        startAdornment: (
                                            <InputAdornment position="start">
                                                <AccountCircleOutlined />
                                            </InputAdornment>
                                        ),
                                    }
                                }

                            }
                        />
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            id="username"
                            label="Nome de Usuário"
                            name="username"
                            autoComplete="username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            slotProps={{

                                input: {
                                    startAdornment: (
                                        <InputAdornment position="start">
                                            <PersonOutline />
                                        </InputAdornment>
                                    ),
                                }
                            }}


                        />
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            id="email"
                            label="Endereço de Email"
                            name="email"
                            autoComplete="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            slotProps={{
                                input: {

                                    startAdornment: (
                                        <InputAdornment position="start">
                                            <EmailOutlined />
                                        </InputAdornment>
                                    ),

                                }
                            }}

                        />
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            id="phone"
                            label="Telefone"
                            name="phone"
                            autoComplete="tel"
                            value={phone}
                            onChange={(e) => setPhone(e.target.value)}
                            slotProps={{
                                input: {
                                    startAdornment: (
                                        <InputAdornment position="start">
                                            <PhoneOutlined />
                                        </InputAdornment>
                                    ),
                                }
                            }}
                            onBlur={onBlurTelefone}
                        />
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            name="password"
                            label="Senha"
                            type={showPassword ? 'text' : 'password'}
                            id="password"
                            autoComplete="new-password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            slotProps={{
                                input: {
                                    endAdornment: (
                                        <InputAdornment position="end">
                                            <IconButton
                                                aria-label="toggle password visibility"
                                                onClick={handleClickShowPassword}
                                                onMouseDown={handleMouseDownPassword}
                                                edge="end"
                                            >
                                                {showPassword ? <VisibilityOff /> : <Visibility />}
                                            </IconButton>
                                        </InputAdornment>
                                    ),
                                    startAdornment: (
                                        <InputAdornment position="start">
                                            <LockOutlinedIcon />
                                        </InputAdornment>
                                    ),
                                }
                            }}
                        />
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            name="confirmPassword"
                            label="Confirmar Senha"
                            type="password"
                            id="confirmPassword"
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                             slotProps={{
                                input: {
                                    endAdornment: (
                                        <InputAdornment position="end">
                                            <IconButton
                                                aria-label="toggle password visibility"
                                                onClick={handleClickShowPassword}
                                                onMouseDown={handleMouseDownPassword}
                                                edge="end"
                                            >
                                                {showPassword ? <VisibilityOff /> : <Visibility />}
                                            </IconButton>
                                        </InputAdornment>
                                    ),
                                    startAdornment: (
                                        <InputAdornment position="start">
                                            <LockOutlinedIcon />
                                        </InputAdornment>
                                    ),
                                }
                            }}
                        />
                        {error && (
                            <Typography color="error" variant="body2" sx={{ mt: 2, textAlign: 'center' }}>
                                {error}
                            </Typography>
                        )}
                        <Button
                            type="submit"
                            fullWidth
                            variant="contained"
                            sx={{ mt: 3, mb: 2 }}
                        >
                            Registrar
                        </Button>
                        <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
                            <Link href="/login" variant="body2">
                                Já tem uma conta? Faça login
                            </Link>
                        </Box>
                    </Box>
                </Box>
            </Container>
        </ThemeRegistry>
    );
}
