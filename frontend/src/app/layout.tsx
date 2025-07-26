import * as React from 'react';
import ThemeRegistry from '../components/ThemeRegistry';


export const metadata = {
  title: 'Ride Finance',
  description: 'Seu controle financeiro na direção certa',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-br">
      <body>
        {/* O ThemeRegistry envolve toda a aplicação, aplicando o tema escuro globalmente */}
        <ThemeRegistry>
          {children}
        </ThemeRegistry>
      </body>
    </html>
  );
}
