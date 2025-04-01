import { useState } from 'react';
import type { ReactElement } from 'react';
import {
  Box,
  Button,
  Textarea,
  Stack,
  Text,
  Badge,
  useToast,
} from '@chakra-ui/react';
import axios from 'axios';

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
}

export const ContentAnalyzer = (): ReactElement => {
  const [content, setContent] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<ContentResponse | null>(null);
  const toast = useToast();

  const handleAnalyze = async () => {
    if (!content.trim()) {
      toast({
        title: 'Please enter some text',
        status: 'warning',
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    setIsLoading(true);
    try {
      const response = await axios.post<ContentResponse>('http://localhost:8000/analyze', {
        text: content
      });
      setAnalysisResult(response.data);
    } catch (error) {
      toast({
        title: 'Error analyzing content',
        description: 'Please try again later',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  const getIssueColor = (type: string): string => {
    switch (type) {
      case 'passive_voice':
        return 'red';
      case 'abbreviation':
        return 'orange';
      case 'complex_word':
        return 'purple';
      case 'contraction':
        return 'blue';
      default:
        return 'gray';
    }
  };

  const highlightIssues = (text: string, issues: ContentIssue[]): ReactElement[] => {
    if (!issues.length) return [<span key="0">{text}</span>];

    const sortedIssues = [...issues].sort((a, b) => a.start - b.start);
    const result: ReactElement[] = [];
    let lastIndex = 0;

    sortedIssues.forEach((issue, index) => {
      if (issue.start > lastIndex) {
        result.push(
          <span key={`text-${index}`}>
            {text.slice(lastIndex, issue.start)}
          </span>
        );
      }
      result.push(
        <Badge
          key={`issue-${index}`}
          colorScheme={getIssueColor(issue.type)}
          variant="subtle"
          title={issue.description}
        >
          {text.slice(issue.start, issue.end)}
        </Badge>
      );
      lastIndex = issue.end;
    });

    if (lastIndex < text.length) {
      result.push(
        <span key="last">{text.slice(lastIndex)}</span>
      );
    }

    return result;
  };

  return (
    <Box width="100%">
      <Box mb={6}>
        <Textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="Enter your text here..."
          size="lg"
          minH="200px"
        />
        <Button
          mt={4}
          colorScheme="blue"
          onClick={handleAnalyze}
          isLoading={isLoading}
        >
          Analyze Content
        </Button>
      </Box>

      {analysisResult && (
        <Stack direction="column" spacing={4}>
          {analysisResult.issues.length > 0 ? (
            <>
              <Text fontSize="lg" fontWeight="bold">
                Found {analysisResult.issues.length} issue(s):
              </Text>
              <Box as="ul" listStyleType="none" ml={0}>
                {analysisResult.issues.map((issue, index) => (
                  <Box as="li" key={index} py={2}>
                    <Badge colorScheme={getIssueColor(issue.type)} mr={2}>
                      {issue.type}
                    </Badge>
                    {issue.description} - {issue.suggestion}
                  </Box>
                ))}
              </Box>
              <Box p={4} borderWidth={1} borderRadius="md">
                <Text fontWeight="bold" mb={2}>
                  Highlighted Text:
                </Text>
                <Text>
                  {highlightIssues(content, analysisResult.issues)}
                </Text>
              </Box>
              <Box p={4} borderWidth={1} borderRadius="md">
                <Text fontWeight="bold" mb={2}>
                  Improved Text:
                </Text>
                <Text>{analysisResult.improved_text}</Text>
              </Box>
            </>
          ) : (
            <Text color="green.500" fontWeight="bold">
              No issues found in your text!
            </Text>
          )}
        </Stack>
      )}
    </Box>
  );
}; 