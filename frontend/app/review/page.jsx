import ResponseCard from "@components/ResponseCard";

const Page = () => {
  return (
    <div className="container mx-auto px-4">
      <div className="grid gap-4 md:grid-cols-2">
        <div>
          <ResponseCard prompt="Prompt 1" />
        </div>
        <div>
          <ResponseCard prompt="Prompt 2" />
        </div>
      </div>
    </div>
  );
};

export default Page;
