import "@styles/globals.css";

import Nav from "@components/Nav";
import Provider from "@components/Provider";
import { StarsCanvas } from "@components/canvas";

export const metadata = {
  title: "convinced",
  description: "Discover & Share AI Prompts",
};

const RootLayout = ({ children }) => (
  <html lang='en'>
    <body>
      <Provider>
        <div className='main'>
          <div className='gradient' />
        </div>

        <main className='app'>
          <Nav />
          {children}
          <StarsCanvas />
        </main>
      </Provider>
    </body>
  </html>
);

export default RootLayout;
