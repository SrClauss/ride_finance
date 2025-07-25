import { GlobalStyles as MuiGlobalStyles } from '@mui/material';

export default function GlobalStyles() {
  return (
    <MuiGlobalStyles
      styles={(theme) => ({
        // Definição da animação fadeIn
        '@keyframes fadeIn': {
          from: {
            opacity: 0,
            transform: 'translateY(20px)',
          },
          to: {
            opacity: 1,
            transform: 'translateY(0)',
          },
        },
        // Classes de utilidade que você pode querer manter
        '.fade-in': {
          animation: 'fadeIn 0.5s ease-in',
        },
        '.shadow-material': {
          boxShadow: '0 2px 4px rgba(0,0,0,0.1), 0 8px 16px rgba(0,0,0,0.1)',
        },
        '.glass-effect': {
          background: 'rgba(30, 30, 30, 0.8)',
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(255, 255, 255, 0.1)',
        },
        // Estilos base para o body
        body: {
          backgroundColor: theme.palette.background.default,
          color: theme.palette.text.primary,
        },
      })}
    />
  );
}