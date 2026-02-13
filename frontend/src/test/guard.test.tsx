import { render } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { vi } from "vitest";

import { LearnPage } from "@/pages/LearnPage";
import { AuthProvider } from "@/lib/auth";

vi.mock("react-router-dom", async (importOriginal) => {
  const actual = await importOriginal<typeof import("react-router-dom")>();
  return {
    ...actual,
    useNavigate: () => vi.fn(),
    useParams: () => ({ courseId: "1", lessonId: "1" }),
  };
});

describe("Learn guard", () => {
  it("renders without crashing for guard flow", () => {
    render(
      <AuthProvider>
        <MemoryRouter>
          <LearnPage />
        </MemoryRouter>
      </AuthProvider>
    );
  });
});
