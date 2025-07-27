// frontend/src/app/payment/page.tsx
'use client';

import * as React from 'react';
import { useRouter } from 'next/navigation';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import Link from '@mui/material/Link';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Chip from '@mui/material/Chip';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Paper from '@mui/material/Paper';

// Ícones do Material-UI
import {
  ArrowBack,
  Check,
  CreditCard,
  OpenInNew,
  Smartphone,
  Star,
  ShieldOutlined,
} from '@mui/icons-material';

import ThemeRegistry from '@/components/ThemeRegistry';

export default function Payment() {
  const router = useRouter();

  const handlePayment = () => {
    // Lógica para abrir o checkout externo
    // const checkoutUrl = 'SUA_URL_DE_CHECKOUT_AQUI';
    // window.open(checkoutUrl, "_blank");
    console.log("Redirecionando para o pagamento...");
    // Por enquanto, vamos simular o redirecionamento para uma página de sucesso ou pendente
    // router.push('/payment-pending');
    alert("Redirecionando para o checkout da Kirvano (simulação).");
  };

  return (
    <ThemeRegistry>
      <Container component="main" maxWidth="sm">
        <CssBaseline />
        <Box
          sx={{
            marginTop: 4,
            marginBottom: 4,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          {/* Cabeçalho */}
          <Box sx={{ width: '100%', display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
             <Button startIcon={<ArrowBack />} onClick={() => router.push('/register')}>
                Voltar
            </Button>
            <Link href="/login" variant="body2" onClick={(e) => {
                e.preventDefault();
                // Adicionar lógica de limpar dados se necessário
                router.push('/login');
            }}>
                Fazer novo login
            </Link>
          </Box>
          
          <Typography component="h1" variant="h4" sx={{ mb: 1, fontWeight: 'bold' }}>
            Finalize seu cadastro
          </Typography>
          <Typography variant="subtitle1" color="text.secondary" sx={{ mb: 4 }}>
            Complete o pagamento para acessar todas as funcionalidades.
          </Typography>

          {/* Card de Preço */}
          <Card sx={{ width: '100%', mb: 4 }}>
            <CardContent sx={{ textAlign: 'center' }}>
              <Chip
                icon={<Star />}
                label="Plano Premium"
                color="success"
                sx={{ mb: 2, fontWeight: 'bold' }}
              />
              <Typography variant="h3" component="div" sx={{ fontWeight: 'bold' }}>
                R$ 2,00
              </Typography>
              <Typography color="text.secondary" sx={{ mb: 2 }}>
                por mês
              </Typography>
              <List sx={{ textAlign: 'left' }}>
                {[
                  'Controle financeiro completo',
                  'Relatórios detalhados',
                  'Backup automático',
                  'Suporte prioritário',
                ].map((text) => (
                  <ListItem key={text} disablePadding>
                    <ListItemIcon>
                      <Check color="success" />
                    </ListItemIcon>
                    <ListItemText primary={text} />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>

          {/* Card de Métodos de Pagamento */}
          <Card sx={{ width: '100%', mb: 4 }}>
             <CardContent>
                <Typography variant="h6" sx={{ textAlign: 'center', mb: 2, fontWeight: 'bold' }}>
                    Formas de pagamento
                </Typography>
                <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center' }}>
                    {/* PIX */}
                    <Paper variant="outlined" sx={{ p: 2, flex: 1, textAlign: 'center', borderColor: 'success.main' }}>
                        <Smartphone color="success" sx={{ fontSize: 40 }}/>
                        <Typography sx={{ fontWeight: 'medium' }}>PIX</Typography>
                        <Chip label="Instantâneo" size="small" color="success" variant="outlined" />
                    </Paper>
                    {/* Cartão */}
                    <Paper variant="outlined" sx={{ p: 2, flex: 1, textAlign: 'center', borderColor: 'primary.main' }}>
                        <CreditCard color="primary" sx={{ fontSize: 40 }}/>
                        <Typography sx={{ fontWeight: 'medium' }}>Cartão</Typography>
                        <Chip label="Aprovação rápida" size="small" color="primary" variant="outlined" />
                    </Paper>
                </Box>
                 <Button
                    onClick={handlePayment}
                    fullWidth
                    variant="contained"
                    startIcon={<OpenInNew />}
                    sx={{ mt: 3, py: 1.5 }}
                >
                    Pagar R$ 2,00 - Kirvano
                </Button>
            </CardContent>
          </Card>

          {/* Informação de Segurança */}
          <Box sx={{ textAlign: 'center', color: 'text.secondary' }}>
            <Typography variant="body2" sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 1 }}>
              <ShieldOutlined fontSize="small" /> Pagamento 100% seguro
            </Typography>
            <Typography variant="caption">
              Processado pela Kirvano com criptografia de ponta a ponta.
            </Typography>
          </Box>
        </Box>
      </Container>
    </ThemeRegistry>
  );
}
