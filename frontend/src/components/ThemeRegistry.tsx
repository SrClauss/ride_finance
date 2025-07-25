'use client';

import * as React from 'react';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import useMediaQuery from '@mui/material/useMediaQuery';
import { getTheme } from "../theme" // Ajuste o caminho se necessário
import GlobalStyles from '../GlobalStyles'; // Ajuste o caminho se necessário


export default function ThemeRegistry({ children }: { children: React.ReactNode }) {
  // Detecta a preferência de tema do sistema operacional para o modo escuro/claro
  const prefersDarkMode = useMediaQuery('(prefers-color-scheme: dark)');
  
  const theme = React.useMemo(
    () => getTheme(prefersDarkMode ? 'dark' : 'light'),
    [prefersDarkMode],
  );

  return (
    <ThemeProvider theme={theme}>
      {/* CssBaseline normaliza os estilos e aplica a cor de fundo base */}
      <CssBaseline />
      {/* Seus estilos globais personalizados e animações */}
      <GlobalStyles />
      {children}
    </ThemeProvider>
  );
}
