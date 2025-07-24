import {Box, Container} from "@mui/material"
import "./globals.css";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html>

      <body>
        
          <Container
          sx={{

            backgroundColor: "#7e0a1cff"
          }}
          
          >

            {children}
          </Container>
      </body>
    </html>
       
  );
}
