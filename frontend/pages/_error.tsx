import { NextPage } from 'next';
import { NextPageContext } from 'next';
import Head from 'next/head';

interface ErrorProps {
  statusCode?: number;
}

const Error: NextPage<ErrorProps> = ({ statusCode }) => {
  return (
    <>
      <Head>
        <title>Error - AI News Agency</title>
      </Head>
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            {statusCode ? `Error ${statusCode}` : 'An Error Occurred'}
          </h1>
          <p className="text-gray-600 mb-4">
            {statusCode === 404
              ? 'This page could not be found.'
              : 'Something went wrong. Please try again.'}
          </p>
          <button
            onClick={() => window.location.href = '/'}
            className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
          >
            Go to Homepage
          </button>
        </div>
      </div>
    </>
  );
};

Error.getInitialProps = ({ res, err }: NextPageContext) => {
  const statusCode = res ? res.statusCode : err ? err.statusCode : 404;
  return { statusCode };
};

export default Error;

