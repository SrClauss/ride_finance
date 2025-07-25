import type { Metadata } from "next";
import { Roboto } from "next/font/google";
import ThemeRegistry from "../components/ThemeRegistry"; // 1. Importe o ThemeRegistry

// Configuração da fonte Roboto otimizada pelo Next.js
const roboto = Roboto({
  weight: ['300', '400', '500', '700'],
  subsets: ['latin'],
  display: 'swap',
});

export const metadata: Metadata = {
  title: "Ride Finance", // Você pode atualizar o título aqui
  description: "Gerenciador financeiro para motoristas de aplicativo",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR">
      <head>
        {/* 2. Adicione o link para o Font Awesome aqui */}
        <link
          rel="stylesheet"
          href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
          crossOrigin="anonymous"
          referrerPolicy="no-referrer"
        />
      </head>
      <body className={roboto.className}>
        {/* 3. Envolva os 'children' com o ThemeRegistry */}
        <ThemeRegistry>
          {children}
        </ThemeRegistry>
      </body>
    </html>
  );
}
