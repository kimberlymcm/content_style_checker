import { useState } from "react";
import type { ReactElement } from "react";
import {
  Box,
  Button,
  Textarea,
  Stack,
  Text,
  Badge,
  useToast,
  Checkbox,
  HStack,
} from "@chakra-ui/react";
import axios from "axios";

interface ContentIssue {
  type: string;
  description: string;
  start: number;
  end: number;
  suggestion: string;
}

interface ContentResponse {
  issues: ContentIssue[];
  improved_text: string;
  llm_details?: {
    prompt: string;
    response: string;
    model: string;
  };
}

export const ContentAnalyzer = (): ReactElement => {
  const [content, setContent] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [useLLM, setUseLLM] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<ContentResponse | null>(
    null,
  );
  const toast = useToast();

  const handleAnalyze = async () => {
    if (!content.trim()) {
      toast({
        title: "Please enter some text",
        status: "warning",
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    setIsLoading(true);
    try {
      const response = await axios.post<ContentResponse>(
        "http://localhost:8000/analyze",
        {
          text: content,
          use_llm: useLLM,
        },
      );
      setAnalysisResult(response.data);
    } catch (error) {
      toast({
        title: "Error analyzing content",
        description: "Please try again later",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  const getIssueColor = (type: string): string => {
    switch (type) {
      case "passive_voice":
        return "red";
      case "abbreviation":
        return "orange";
      case "complex_word":
        return "purple";
      case "contraction":
        return "blue";
      case "third_person":
        return "green";
      default:
        return "gray";
    }
  };

  const highlightIssues = (
    text: string,
    issues: ContentIssue[],
  ): ReactElement[] => {
    if (!issues.length)
      return [
        <span key="0" data-oid="brapr8g">
          {text}
        </span>,
      ];

    const sortedIssues = [...issues].sort((a, b) => a.start - b.start);
    const result: ReactElement[] = [];
    let lastIndex = 0;

    sortedIssues.forEach((issue, index) => {
      if (issue.start > lastIndex) {
        result.push(
          <span key={`text-${index}`} data-oid="v-mv13p">
            {text.slice(lastIndex, issue.start)}
          </span>,
        );
      }
      result.push(
        <Badge
          key={`issue-${index}`}
          colorScheme={getIssueColor(issue.type)}
          variant="subtle"
          title={issue.description}
          data-oid="ti_yvf:"
        >
          {text.slice(issue.start, issue.end)}
        </Badge>,
      );
      lastIndex = issue.end;
    });

    if (lastIndex < text.length) {
      result.push(
        <span key="last" data-oid="nta99a0">
          {text.slice(lastIndex)}
        </span>,
      );
    }

    return result;
  };

  return (
    <Box width="100%" data-oid="93yszd1">
      <Box mb={6} data-oid="cu.lj8k">
        <Textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="Enter your text here..."
          size="lg"
          minH="200px"
          data-oid="lfx2okm"
        />

        <HStack mt={4} spacing={4} data-oid="y08i7a6">
          <Checkbox
            isChecked={useLLM}
            onChange={(e) => setUseLLM(e.target.checked)}
            colorScheme="blue"
            data-oid="zy7zcbb"
          >
            Use AI for enhanced analysis
          </Checkbox>
          <Button
            colorScheme="blue"
            onClick={handleAnalyze}
            isLoading={isLoading}
            data-oid="h.03.x2"
          >
            Analyze Content
          </Button>
        </HStack>
      </Box>

      {analysisResult && (
        <Stack direction="column" spacing={4} data-oid="4bd:dy8">
          {analysisResult.issues.length > 0 ? (
            <>
              <Text fontSize="lg" fontWeight="bold" data-oid="jpunmuu">
                Found {analysisResult.issues.length} issue(s):
              </Text>
              <Box as="ul" listStyleType="none" ml={0} data-oid="lazungr">
                {analysisResult.issues.map((issue, index) => (
                  <Box as="li" key={index} py={2} data-oid="ijaj9bo">
                    <Badge
                      colorScheme={getIssueColor(issue.type)}
                      mr={2}
                      data-oid="rejtzjv"
                    >
                      {issue.type}
                    </Badge>
                    {issue.description} - {issue.suggestion}
                  </Box>
                ))}
              </Box>
              <Box p={4} borderWidth={1} borderRadius="md" data-oid="gg36j89">
                <Text fontWeight="bold" mb={2} data-oid="y1nn.hu">
                  Highlighted Text:
                </Text>
                <Text data-oid="j-js:gh">
                  {highlightIssues(content, analysisResult.issues)}
                </Text>
              </Box>
              <Box p={4} borderWidth={1} borderRadius="md" data-oid="wr4-4c9">
                <Text fontWeight="bold" mb={2} data-oid="6gzps-8">
                  Improved Text:
                </Text>
                <Text data-oid="6oswiah">{analysisResult.improved_text}</Text>
              </Box>
              {analysisResult.llm_details && (
                <Box
                  p={4}
                  borderWidth={1}
                  borderRadius="md"
                  bg="gray.50"
                  data-oid="od5x.s_"
                >
                  <Text
                    fontSize="lg"
                    fontWeight="bold"
                    mb={4}
                    data-oid="z5fql.j"
                  >
                    AI Analysis Details
                  </Text>
                  <Stack spacing={4} data-oid="sqy-9t4">
                    <Box data-oid="ag6ou8x">
                      <Text fontWeight="bold" data-oid="qt_2mz1">
                        Model:
                      </Text>
                      <Text data-oid="p7l66se">
                        {analysisResult.llm_details.model}
                      </Text>
                    </Box>
                    <Box data-oid="zgjzaag">
                      <Text fontWeight="bold" data-oid="00o5hfj">
                        Prompt:
                      </Text>
                      <Box
                        p={2}
                        bg="white"
                        borderRadius="md"
                        whiteSpace="pre-wrap"
                        data-oid="e8768yd"
                      >
                        {analysisResult.llm_details.prompt}
                      </Box>
                    </Box>
                    <Box data-oid="xqo4ve7">
                      <Text fontWeight="bold" data-oid="vhdqerj">
                        Response:
                      </Text>
                      <Box
                        p={2}
                        bg="white"
                        borderRadius="md"
                        whiteSpace="pre-wrap"
                        data-oid="1w3h-5m"
                      >
                        {analysisResult.llm_details.response}
                      </Box>
                    </Box>
                  </Stack>
                </Box>
              )}
            </>
          ) : (
            <Text color="green.500" fontWeight="bold" data-oid="u0sn_.t">
              No issues found in your text!
            </Text>
          )}
        </Stack>
      )}
    </Box>
  );
};
