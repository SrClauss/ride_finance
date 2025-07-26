import { createTheme, responsiveFontSizes, ThemeOptions } from '@mui/material/styles';
import { deepmerge } from '@mui/utils';

// Opções de tema base
const commonSettings: ThemeOptions = {
  shape: {
    borderRadius: 12,
  },
  typography: {
    fontFamily: [
      'Roboto',
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif',
    ].join(','),
  },
};

// Função que cria e retorna o tema configurado
export const getTheme = (mode: 'light' | 'dark') => {
  const theme = createTheme(deepmerge(commonSettings, {
    palette: {
      mode,
      ...(mode === 'dark'
        ? {
            // Paleta de cores para o MODO ESCURO
            primary: { main: 'hsl(207, 90%, 54%)' },
            error: { main: '#f44336' },
            text: {
              primary: '#FFFFFF',
              secondary: 'hsl(240, 5%, 64.9%)',
            },
            background: {
              // AQUI VOCÊ PODE MUDAR A COR DE FUNDO DA PÁGINA PARA OS SEUS TESTES
              default: '#121212', 
              paper: '#1E1E1E', // Cor de fundo para elementos como o Card
            },
            divider: 'rgba(255, 255, 255, 0.12)',
          }
        : {
            // Paleta de cores para o MODO CLARO
            primary: { main: 'hsl(207, 90%, 54%)' },
            background: { default: '#FFFFFF', paper: '#F5F5F5' },
          }),
    },
    components: {
        MuiInputLabel: {
            styleOverrides: {
                root: {
                    color: 'hsl(240, 5%, 64.9%)',
                    '&.Mui-focused': { color: 'hsl(207, 90%, 54%)' }
                }
            }
        },
        MuiInputBase: {
            styleOverrides: {
                input: ({ theme }) => ({
                    // Define o esquema de cores para o input, melhorando a compatibilidade
                    // com o autofill do Firefox em temas escuros, que era o ponto que faltava.
                    colorScheme: 'dark',

                    '&:-webkit-autofill, &:-webkit-autofill:hover, &:-webkit-autofill:focus, &:-webkit-autofill:active': {
                        // O truque da sombra interna para forçar a cor de fundo.
                        // Usamos !important, como você sugeriu, para garantir a sobreposição.
                        WebkitBoxShadow: `0 0 0 100px ${theme.palette.background.paper} inset !important`,
                        // Força a cor do texto usando o tema e !important.
                        WebkitTextFillColor: `${theme.palette.text.primary} !important`,
                        // Garante que a cor do cursor (caret) seja consistente.
                        caretColor: theme.palette.text.primary,
                        borderRadius: 'inherit',
                        // O "HACK" DA TRANSIÇÃO LONGA: engana o navegador para não aplicar o seu estilo.
                        transition: 'background-color 5000s ease-in-out 0s',
                    },
                    // Mantém o espaçamento interno
                    paddingLeft: '8px !important',
                }),
            }
        },
        MuiOutlinedInput: {
            styleOverrides: {
                root: {
                    // Mantém o fundo sólido para garantir consistência visual
                    backgroundColor: '#1E1E1E',
                    '&:hover': {
                        backgroundColor: '#1E1E1E',
                    },
                    '&.Mui-focused': {
                        backgroundColor: '#1E1E1E',
                    },

                    '& .MuiInputAdornment-positionStart': { marginLeft: '8px' },
                    '& .MuiOutlinedInput-notchedOutline': { borderColor: 'rgba(255, 255, 255, 0.23)' },
                    '&:hover .MuiOutlinedInput-notchedOutline': { borderColor: 'rgba(255, 255, 255, 0.5)' },
                    '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                        borderColor: 'hsl(207, 90%, 54%)',
                        borderWidth: '1px',
                    },
                },
            },
        },
    }
  }));
  
  return responsiveFontSizes(theme);
}
  