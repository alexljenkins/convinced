import "@styles/globals.css";

import Nav from "@components/Nav";
import { StarsCanvas } from "@components/canvas";

export const metadata = {
  title: "convinced",
  description: "Practice writing with impact",
};

const RootLayout = ({ children }) => (
  <html lang='en'>
    <body>
        <div className='main'>
          <div className='gradient' />
        </div>

        <main className='app'>
          <Nav />
          {children}
          <StarsCanvas />
        </main>
    </body>
  </html>
);

export default RootLayout;
